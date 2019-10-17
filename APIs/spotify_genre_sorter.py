# This code uses the Spotify API and Spotipy library to take in a spotify playlist URI
# as an input and sorts the tracks of the playlist by decade into new saved playlists.

# Authentication Steps
import spotipy.util as util
username = "my_username"
scope = "user-library-read"
client_id = "my_client_id"
client_secret = "my_client_secret"
redirect_uri = "http://localhost/"
token = util.prompt_for_user_token(username, scope,client_id,client_secret,redirect_uri)

import spotipy
sp = spotipy.Spotify(token)

def sort_playlist_by_genre(playlist_uri):
	result = sp.user_playlist(username, playlist_uri)
	playlist_name = result['name']
	# All Playlist Information
	playlists = sp.current_user_playlists()
	items = playlists['items']
	# Create Playlist and URI Dictionary
	playlist_name_uri_dict = {}
	for item in items:
	    playlist_uri = item['uri']
	    playlist_name_uri_dict[item['name']] = playlist_uri
	# Create Playlist Name for each Track
	tracks = result['tracks']['items']
	for i in range(len(tracks)):
	    name = tracks[i]['track']['name']
	    album = tracks[i]['track']['album']
	    uri = tracks[i]['track']['uri']
	    release_date = album['release_date']
	    year = release_date[:4]
	    decade = str(year[2]) + "0" 
	    new_playlist_name = decade + "'s " + playlist_name
	    # If Playlist Exists Add Track
	    if new_playlist_name in playlist_name_uri_dict:
	        playlist_uri = playlist_name_uri_dict[new_playlist_name]
	        sp.user_playlist_add_tracks(username, playlist_uri, [uri], position = None)
	    # Otherwise Create Playlist and Add Track
	    else:
	        new_playlist = sp.user_playlist_create(username, new_playlist_name)
	        playlist_uri = new_playlist['uri']
	        sp.user_playlist_add_tracks(username, playlist_uri, [uri], position = None)
	        playlist_name_uri_dict[new_playlist_name] = playlist_uri
	return

# Accept User Input
spotify_uri = input("Spotify URI: ")
sort_playlist_by_genre(spotify_uri)