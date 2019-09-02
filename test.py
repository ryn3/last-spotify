import pylast
import time

class LastExtract(object):
    def __init__(self):
        
    def get_track_list(self, api_key, api_secret, username, password):

        API_KEY = '86530cb3204f829e6a1f1c05d61bf230'
        API_SECRET = 'f338589f5f80231349672dd48cf5b50b'
        username = 'verve3349'
        password_hash = pylast.md5('Leeryan14*')

        n = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)
        
        #p = pylast.Library(user='verve3349', network=n)
        #print(p.get_artists())
        
        u = pylast.User(user_name=username,network=n)
        
        time_input = input("input initial time [yr]:[mon]:[day] i.e. 190101, 191230 --   ")
        init_time = int(time.mktime(time.strptime(time_input+"", "%y%m%d")))
        
        time_input = input("input final time [yr]:[mon]:[day] i.e. 190101, 191230 --   ")
        final_time = int(time.mktime(time.strptime(time_input+"", "%y%m%d")))
        
        tag_input = input("input a tag: ")
        
        print("init time: "+str(init_time))
        print("final_time: "+str(final_time))
        print("tag_input: "+tag_input)
        
        recent_tracks = u.get_recent_tracks(limit=100,time_from=init_time, time_to=final_time)
        track_list = []
        for track in recent_tracks:
            album = track.album
            artist = track.track.artist
            o = pylast._Opus(artist=artist,title=album,network=n,ws_prefix='album',username=username)
            tags = artist.get_top_tags(limit=10)
            tag_list = []
            for tag in tags:
                tag = tag.item
                tag_name = tag.get_name()
                tag_list.append(tag_name)
            if tag_input in tag_list:
                track_list.append(track)
                print(str(artist)+": "+str(album))
        track_list = list(dict.fromkeys(track_list))
        return track_list
        
        
