import requests
import json
import urllib3

from notification import run_terminal_command

# Suppress only the single InsecureRequestWarning from urllib3 needed for unverified HTTPS requests.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Replace this with the playlist ID of the playlist you want to add the song to
playlist_id = "5bOP6JdynwJrbYXpKiUw61"

def get_currently_playing_track(token):
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers, verify=False)
    response_data = response.json()
    if response.status_code == 204 or response_data == {}:
        return None
    return response_data.get('item', {}).get('id')

def add_track_to_playlist(token, track_id):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris=spotify:track:{track_id}'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, verify=False)
    if response.status_code == 201:
        print('Track added to playlist successfully!')
    else:
        handle_error(response, "Error Adding Track to Playlist")

def add_track_to_liked_songs(token, track_id):
    url = f'https://api.spotify.com/v1/me/tracks?ids={track_id}'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, verify=False)
    if response.status_code == 200:
        print('Track added to liked songs successfully!')
    else:
        handle_error(response, "Error Adding Track to Liked Songs")

def handle_error(response, title):
    try:
        error_data = response.json()
        error_message = error_data.get('error', {}).get('message', 'Unknown error')
    except json.JSONDecodeError:
        error_message = response.text
    print(f'{title}: {error_message}')
    run_terminal_command(error_message, 'error')