# This code is an exercise based on the video tutorial found at https://www.youtube.com/watch?v=XQgXKtPSzUI 
# It uses web scraping to extract the title, artist and album of the first 30 songs from the "Today's Top Hits" 
# playlist on spotify. This information is then written to a CSV file entitled "spotify_tracks.csv".

from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

spotify_url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"

uClient = urlopen(spotify_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div", "tracklist-col name") 

filename = "spotify_tracks.csv"
f = open(filename, 'w')

header = "track_name, track_artist, track_album\n"

f.write(header)

for container in containers:
	track_name = container.find("span","track-name").text

	artist_album_info = container.find("span","artists-albums")
	if artist_album_info:
	    track_artist = artist_album_info.findAll("span",{"dir":"auto"})[0].text
	    track_album = artist_album_info.findAll("span",{"dir":"auto"})[1].text
	else:
	    track_artist = "Not Specified"
	    track_album = "Not Specified"

	f.write(track_name.replace(",","|") + "," + track_artist.replace(",","|") + "," + track_album.replace(",","|") + "\n")

f.close()
