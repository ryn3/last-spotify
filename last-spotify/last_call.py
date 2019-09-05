import pylast
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import pprint

class LastExtract(object):
    def __init__(self):
        self.track_list = []
        self.track_ids = []

    def get_track_list(self):

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
            #print(str(artist) +": "+str(title))
            #print(tag_list)
            #print()
            for tag_item in tag_list: 
                if tag_input.lower() in tag_item.lower():
                    #track_list.append(track)
                    track_item = str(artist)+" "+str(title)
                    track_list.append(track_item)
                    print(track.playback_date+" -- "+track_item)
        track_list = list(dict.fromkeys(track_list))
        #print(track_list)
        self.track_list = track_list
        return track_list

    def get_track_id(self, search_str):
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
        all_ids = []
        for track in self.track_list:
            id = self.get_track_id(track)
            if len(id) > 0:
                all_ids.append(id)
        self.track_ids = all_ids
        return all_ids

    def normalize(self, string):
        string = string.lower()
        remove_words = ["the", "a", "an"]
        if string.find("the ") == 0 or string.find("a ") == 0:
            string = string.replace("the ", '')
        return string








