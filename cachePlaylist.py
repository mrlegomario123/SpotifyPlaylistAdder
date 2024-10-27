import pickle
import os
import requests

# File to store the playlist cache
playlist_cache_file = "./LocalData/playlist_cache.pkl"

# Cache for playlist tracks
playlist_cache = set()

# Replace this with the playlist ID of the playlist you want to add the song to
playlist_id = "5bOP6JdynwJrbYXpKiUw61"

def cache_playlist_tracks(token):
    global playlist_cache
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    playlist_cache.clear()
    while url:
        response = requests.get(url, headers=headers, verify=False)
        response_data = response.json()
        for item in response_data['items']:
            playlist_cache.add(item['track']['id'])
        url = response_data.get('next')
    print(f"Cached {len(playlist_cache)} tracks from the playlist.")
    with open(playlist_cache_file, 'wb') as f:
        pickle.dump(playlist_cache, f)

def load_playlist_cache():
    global playlist_cache
    if os.path.exists(playlist_cache_file):
        with open(playlist_cache_file, 'rb') as f:
            playlist_cache = pickle.load(f)
        print(f"Loaded {len(playlist_cache)} tracks from the cache file.")

def is_track_in_playlist(track_id):
    return track_id in playlist_cache