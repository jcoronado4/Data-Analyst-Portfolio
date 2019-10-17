# This code uses the Spotify API and Spotipy library to create a CSV file for each of
# my chosen playlists. Each CSV contains information for every track in the playlist
# along with the date the track was added to the file. When rerun it appends any new 
# tracks to the CSV. A new folder and files are created each year.

# Future Updates: Automatically run this program at scheduled times.

# Authentication Steps
import spotipy.util as util
username = "my_username"
scope = "user-library-read"
client_id = "my_client_id"
client_secret = "my_client_secret"
redirect_uri = "http://localhost/"
token = util.prompt_for_user_token(username, scope,client_id,client_secret,redirect_uri)

# Global Info
import spotipy
import datetime
import os
sp = spotipy.Spotify(token)
now = datetime.datetime.now()
current_month = now.strftime("%B")
current_year = now.year
today = current_month + " " + str(now.day)

# Create Folders
sp_path = os.path.join("Spotify", str(current_year))
os.makedirs(sp_path, exist_ok = True)

# Return Track Info as a String
def get_track_info(tracks):
	name = tracks['track']['name'].replace(",","|")
	artist = tracks['track']['artists'][0]['name'].replace(",","|")
	album = tracks['track']['album']['name'].replace(",","|")
	return(name + "," + artist + "," + album)

# Creates a CSV File for Each Playlist
def playlist_tracks_file(username, uri):
    results = sp.user_playlist(username, uri)
    playlist_name = results['name']
    filename = playlist_name + " - " + str(current_year) + ".csv"
    file_path = os.path.join(sp_path,filename)
    # If File Exists Append New Tracks
    if os.path.exists(file_path):
    	f = open(file_path, 'r')
    	csv_contents = f.read()
    	f.close()
    	f = open(file_path, 'a')
    	tracks = results['tracks']['items']
    	for i in range(len(tracks)):
    		track_info = get_track_info(tracks[i])
    		if not track_info in csv_contents:
        		f.write(track_info + "," + today + "\n")
    # Otherwise Create New File
    else:
    	f = open(file_path, 'w')
    	header = "Name" + "," + "Artist" + "," + "Album" + "," + "Date Added to File\n"
    	f.write(header)
    	tracks = results['tracks']['items']
    	for i in range(len(tracks)):
        	track_info = get_track_info(tracks[i])
        	f.write(track_info + "," + today + "\n")
    f.close()
    return

# Creates a CSV File for my Liked Songs
def liked_songs_tracks_file():
	lim = 50
	filename = "Liked Songs" + " - " + str(current_year) + ".csv"
	file_path = os.path.join(sp_path,filename)
    # If File Exists Append New Tracks
	if os.path.exists(file_path):
		f = open(file_path, 'r')
		csv_contents = f.read()
		f.close()
		f = open(file_path, 'a')
		try:
		    tracks = sp.current_user_saved_tracks(limit = lim)
		    total_tracks = tracks['total']
		    off_index = lim
		    num_iter = total_tracks // lim
		    for i in range(num_iter):
		        for track in tracks['items']:
		        	track_info= get_track_info(track)
		        	if not track_info in csv_contents:
		        		f.write(track_info + "," + today + "\n")
		        tracks = sp.current_user_saved_tracks(limit = lim, offset = off_index)
		        off_index = off_index + lim
		    for track in tracks['items']:
		    	track_info= get_track_info(track)
		    	if not track_info in csv_contents:
		    		f.write(track_info + "," + today + "\n")
		except:
		    pass
    # Otherwise Create New File
	else:
		f = open(file_path, 'w')
		header = "Name" + "," + "Artist" + "," + "Album" + "," + "Date Added to File\n"
		f.write(header)
		try:
		    tracks = sp.current_user_saved_tracks(limit = lim)
		    total_tracks = tracks['total']
		    off_index = lim
		    num_iter = total_tracks // lim
		    for i in range(num_iter):
		        for track in tracks['items']:
		        	track_info= get_track_info(track)
		        	f.write(track_info + "," + today + "\n")
		        tracks = sp.current_user_saved_tracks(limit = lim, offset = off_index)
		        off_index = off_index + lim
		    for track in tracks['items']:
		        track_info= get_track_info(track)
		        f.write(track_info + "," + today + "\n")
		except:
		    pass
	f.close()
	return

# Create "Today's Top Hits" CSV File 
playlist_tracks_file("Spotify", "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M")

# Create "Rock This" CSV File
playlist_tracks_file("Spotify", "spotify:playlist:37i9dQZF1DXcF6B6QPhFDv")

# Create "Viva Latino" CSV File
playlist_tracks_file("Spotify", "spotify:playlist:37i9dQZF1DX10zKzsJ2jva")

# Create "Alternative Beats" CSV File
playlist_tracks_file("Spotify", "spotify:playlist:37i9dQZF1DWXMg4uP5o3dm")

# Create "Pop Remix" CSV File
playlist_tracks_file("Spotify", "spotify:playlist:37i9dQZF1DXcZDD7cfEKhW")

# Create "Liked Songs" CSV File
liked_songs_tracks_file()
