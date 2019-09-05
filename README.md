# last-spotify

This app creates Spotify playlists based on your Last.fm scrobbles. Input a scrobble date-range and a tag (genre/subgenre) to retrieve your songs for your playlist. The app by default filters any duplicates. 

**Using this app requires that you have at least some scrobbles, as the playlists only contains previously played songs**

## Dependencies
	
	$ pip3 install -r requirements.txt

## Usage

### 1. Create Last.fm API Account (Authentication pt 1)

Go to <https://www.last.fm/api/account/create> and create your API account. Your redirect uri can be anything. If you're unsure of what to put you can input https://verve3349.wordpress.com/.

Be sure to immediately copy your API key and secret, since last.fm doesn't allow you to access this information again. Then, in `last_call.py enter all your last.fm info into the first four variables under the get_track_list method.

### 1.5. Create Spotify App (Authentication pt 2)

Sign in to Spotify and go to <https://www.developer.spotify.com/dashboard/applications> in order to create your own application with unique client id, secret, and redirect uri. 

Using the text editor of your choice, paste your client id, secret, and redirect uri into the variables found in `spotify-creds.sh

Then,

	$ cd last-spotify
	$ cat spotify-creds.sh

Copy and paste the lines with your completed authentication info into the command line. You should get something like this:

	$ export SPOTIPY_CLIENT_ID = [client_id]
	$ export SPOTIPY_CLIENT_SECRET = [client_secret]
	$ export SPOTIPY_REDIRECT_URI = [redirect_uri]

### 2. Create playlist

	$ python3 spotify_call.py [spotify-id] [playlist-name] [playlist-description]

	i.e.
	$ python3 spotify_call.py 125088194 classical-music-5/19 "Classical music from May 2019"

### 3. Enter scrobble parameters
	
Select the time period you want. For example inputting 190601 and 190701 will tell the app to read your scrobbles from June 1st, 2019 to July 1st, 2019. 

	input initial time [yr][mon][day] i.e. 190101, 191230 --   [input your initial time]
	input final time [yr][mon][day] i.e. 190101, 191230 --   [input your final time]

Then input a single tag (for the purposes of this app, this is the equivalent of genre/subgenre) to tell the app which tag to put into the playlist. Continuing from the above inputs, the tag 'classical' will retrieve scrobbles containing the tag 'classical' from 6/1/19 to 7/1/19. 

**I've chosen to use artist tags, as I've found that these tags usually have more accurate and precise information on the inidividual track genre/subgenre. For example, "Tea Leaf Dancers" by Flying Lotus will return artist tags from the artist, Flying Lotus.**

 

 
