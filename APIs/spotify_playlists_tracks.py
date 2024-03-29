# This code starts by creating a CSV file for each of my chosen playlists.
# Each CSV contains information for every track in the playlist along with 
# the date the track was added to the file. When rerun it appends new 
# tracks to the playlist. A new folder and files are created each year.
# Outputs a TXT file containing times when the program was run.

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
    uri = tracks['track']['uri']
    return(name + "," + artist + "," + album + "," + uri)

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
        	if not tracks[i]['track'] == None:
        		# Get track info if the object is a track
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
        	if not tracks[i]['track'] == None:
        		track_info = get_track_info(tracks[i])
        		f.write(track_info + "," + today + "\n")
    f.close()

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

# Create Text File Showing When Code was Run
filename = "spotify_playlist_tracks.txt"
if os.path.exists(filename):
    f = open(filename, 'a')
    f.write(str(now) + "\n")

else:
    f = open(filename, 'w')
    f.write("spotify_playlist_tracks.py was run at the following times: \n")
    f.write("\n")
    f.write(str(now) + "\n")
f.close()
