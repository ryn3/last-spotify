import pylast
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import pprint

class LastExtract(object):
    """
        This class interacts with Last.fm's and Spotify's Python client.
        It will get your scrobbles, and the associated Spotify track IDs.

    """
    def __init__(self):
        """
            self.track_list is a list of scrobbles (TopTracks)
            self.track_ids is a list of Spotify IDs
        
        """
        self.track_list = []
        self.track_ids = []

    def get_track_list(self):
        """
            Returns a list of your scrobbles given your inputted date range and tag.

        """
        API_KEY = 'paste your API key here'
        API_SECRET = 'paste your API secret here'
        username = 'enter your username'
        password_hash = pylast.md5('enter your password')
        n = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)
        u = pylast.User(user_name=username,network=n)
        time_input = input("input initial time [yr][mon][day] i.e. 190101, 191230 --   ")
        init_time = int(time.mktime(time.strptime(time_input+"", "%y%m%d")))
        time_input = input("input final time [yr][mon][day] i.e. 190101, 191230 --   ")
        final_time = int(time.mktime(time.strptime(time_input+"", "%y%m%d")))
        tag_input = input("input a tag: ")
        recent_tracks = u.get_recent_tracks(limit=1000,time_from=init_time, time_to=final_time)
        track_list = []

        for track in recent_tracks:
            title = track.track.title
            album = track.album
            artist = track.track.artist
            o = pylast._Opus(artist=artist,title=album,network=n,ws_prefix='album',username=username)
            tags = artist.get_top_tags(limit=10)
            tag_list = []
            for tag in tags:
                tag = tag.item
                tag_name = tag.get_name()
                tag_list.append(tag_name)
            for tag_item in tag_list: 
                if tag_input.lower() in tag_item.lower():
                    track_item = str(artist)+" "+str(title)
                    track_list.append(track_item)
                    print(track.playback_date+" -- "+track_item) #print scrobble
        track_list = list(dict.fromkeys(track_list)) #eliminate duplicates
        self.track_list = track_list
        return track_list

    def get_track_id(self, search_str):
        """
            search_str: this string acts as a query ([artist] [track name]) for the Spotify Client
            returns the Spotify track ID of the query

        """
        client_credentials_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        normal = self.normalize(search_str)
        result = sp.search(normal)
        final_results = []
        for each in result["tracks"]["items"]:
            track = each["name"]
            artist = each["album"]["artists"][0]["name"]
            if track.lower() in search_str.lower() and artist.lower() in search_str.lower():
                final_results.append(each["id"])
        try:
            final_results = final_results[0]
        except:
            n=0
        return final_results
     
    def get_all_ids(self): 
        """
            Iterates through all your scrobbles to get Spotify IDs
        
        """
        all_ids = []
        for track in self.track_list:
            id = self.get_track_id(track)
            if len(id) > 0:
                all_ids.append(id)
        self.track_ids = all_ids
        return all_ids

    def normalize(self, string):
        """
            string: this is your Spotify query (search_str from get_track_id method)
            returns a normalized string for optimized Spotify track search

        """
        string = string.lower()
        remove_words = ["the", "a", "an"]
        if string.find("the ") == 0 or string.find("a ") == 0:
            string = string.replace("the ", '')
        return string








