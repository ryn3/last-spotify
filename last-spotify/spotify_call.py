import last_call
import pprint
import sys
import os
import subprocess
import spotipy
import spotipy.util as util

def create_playlist():
    """
        Interacts with spotipy
        Initializes a Spotify playlist with a name and description 

    """
    id = ''
    if len(sys.argv) > 2:
        username = sys.argv[1]
        playlist_name = sys.argv[2]
        playlist_description = sys.argv[3]
    else:
        print("Usage: %s username playlist-name playlist-description" % (sys.argv[0],))
        sys.exit()
    
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username,scope=scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlists = sp.user_playlist_create(user=username, name=playlist_name, description=playlist_description)
        id = playlists["id"]
    else:
        print("Can't get token for", username)
    return id
                                                
def get_ids():
    """
        Initializes LastExtract object and returns Spotify track IDs of your scrobbles

    """
    t = last_call.LastExtract()
    track_list = t.get_track_list()
    track_ids = t.get_all_ids()
    return track_ids

def add_tracks(p_id, t_id):
    """
        p_id: Spotify playlist ID of initialized playlist
        t_id: list of track IDs to add into playlist
        adds tracks into the playlist

    """
    if len(sys.argv) > 3:
        username = sys.argv[1]
        playlist_id = p_id
        track_ids = t_id
    else:
        print("Usage: %s username playlist_id track_id ..." % (sys.argv[0],))
        sys.exit()

    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
        print("Tracks have been added to your playlist.")
    else:
        print("Can't get token for", username)


id = create_playlist()
tracks = get_ids()
while tracks:
    try:
        temp = []
        next_list = []
        temp = tracks[:99]
        add_tracks(id,temp)
        tracks = tracks[99:]
    except:
        print('done')

