from spotifyAuth import get_valid_token
from spotifyClient import get_currently_playing_track, add_track_to_playlist, add_track_to_liked_songs
from cachePlaylist import cache_playlist_tracks, load_playlist_cache, is_track_in_playlist
from notification import run_terminal_command
import os

def main():
    try:
        token = get_valid_token()
        load_playlist_cache()
        track_id = get_currently_playing_track(token)
        if track_id:
            print(f"Currently playing track ID: {track_id}")
            add_track_to_liked_songs(token, track_id)
            if not is_track_in_playlist(track_id):
                add_track_to_playlist(token, track_id)
                run_terminal_command("Song added to playlist", 'Playlist Updated')
            else:
                print("Track is already in the playlist.")
                run_terminal_command("Song already in playlist", 'Song Already Added')
            cache_playlist_tracks(token)
    except Exception as e:
        print('Error:', e)
        run_terminal_command(str(e), 'Error Adding Song')

if __name__ == '__main__':
    main()