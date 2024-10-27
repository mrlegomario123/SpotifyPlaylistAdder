import requests
import base64
import time
import threading
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
import subprocess

from notification import run_terminal_command

# Replace these with your Spotify app credentials
client_id = "01b6b299a49443bebe5926dfbbd4736b"
client_secret = "54a8ff0f23a94736b3038e43fee6e70f"
redirect_uri = 'http://localhost:8888/callback'

# Global variable to store the authorization code
auth_code = None

# Files to store the tokens
access_token_file = "./LocalData/access_token.json"
refresh_token_file = "./LocalData/refresh_token.txt"

# Ensure the LocalData directory exists
os.makedirs("./LocalData", exist_ok=True)

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query_components = parse_qs(urlparse(self.path).query)
        auth_code_list = query_components.get('code')
        if auth_code_list:
            auth_code = auth_code_list[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'<html><body><p>Authorization successful! You can close this window.</p><script>window.close();</script></body></html>')
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'<html><body><p>Authorization failed. No code parameter found.</p></body></html>')

def start_http_server():
    server_address = ('', 8888)
    httpd = HTTPServer(server_address, OAuthHandler)
    httpd.serve_forever()

def get_oauth_token():
    global auth_code
    auth_url = 'https://accounts.spotify.com/authorize'
    token_url = 'https://accounts.spotify.com/api/token'
    auth_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': 'user-read-playback-state playlist-modify-public playlist-modify-private user-library-modify'
    }
    
    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=start_http_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Open the authorization URL in the default web browser
    auth_response = requests.get(auth_url, params=auth_params, verify=False)
    authorization_url = auth_response.url

    # Automatically open the URL in the default web browser in the background
    subprocess.run(['open', '-g', authorization_url])

    run_terminal_command(f"Follow the steps in the opened browser window, run from terminal sudo python3 main.py", 'Authorize Spotify')
    print(f"Please go to the following URL and authorize the application: {authorization_url}")
    
    # Wait for the authorization code to be set by the HTTP server
    while auth_code is None:
        time.sleep(1)
    
    token_headers = {
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri
    }
    response = requests.post(token_url, headers=token_headers, data=token_data, verify=False)
    response_data = response.json()
    
    # Save the access token and expiration time to a file
    access_token_info = {
        'access_token': response_data['access_token'],
        'expires_at': time.time() + response_data['expires_in']
    }
    with open(access_token_file, 'w') as f:
        json.dump(access_token_info, f)
    
    # Save the refresh token to a separate file
    with open(refresh_token_file, 'w') as f:
        f.write(response_data['refresh_token'])
    
    return response_data['access_token']

def refresh_oauth_token():
    token_url = 'https://accounts.spotify.com/api/token'
    with open(refresh_token_file, 'r') as f:
        refresh_token = f.read().strip()
    token_headers = {
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(token_url, headers=token_headers, data=token_data, verify=False)
    response_data = response.json()
    
    # Update the access token info with the new access token and expiration time
    access_token_info = {
        'access_token': response_data['access_token'],
        'expires_at': time.time() + response_data['expires_in']
    }
    with open(access_token_file, 'w') as f:
        json.dump(access_token_info, f)
    
    return response_data['access_token']

def get_valid_token():
    if not os.path.exists(refresh_token_file):
        return get_oauth_token()
    if not os.path.exists(access_token_file):
        # Create an empty access token file if it doesn't exist
        with open(access_token_file, 'w') as f:
            json.dump({}, f)
        return get_oauth_token()
    
    with open(access_token_file, 'r') as f:
        access_token_info = json.load(f)
    
    # Check if the access token is close to expiring (within 10 minutes) or has expired
    if 'access_token' in access_token_info and time.time() < access_token_info['expires_at'] - 600:
        return access_token_info['access_token']
    else:
        return refresh_oauth_token()