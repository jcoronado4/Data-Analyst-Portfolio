# This code uses the billboard.py API to extract information from a given 
# billboard chart in a given time frame. It creates a folder and file for
# each year in the time frame and outputs CSV files containing the track 
# title and artist.

import billboard
import time
import os

# Creates the CSV filename based on the chart name given
def get_file_name(name):
	filename = ""
	for i in range(len(name)):
	    if i == 0:
	        filename = filename + name[i].upper()
	    elif name[i-1] == "-":
	        filename = filename + name[i].upper()
	    else:
	        filename = filename + name[i]
	filename = filename.replace("-"," ")
	return(filename)

# Writes track information into the CSV file
def file_writer(f, chart_name, year, tracks_string):
	# Iterates through the first day of each month for the given year
	for j in range(12):
		month = f"{j+1:02d}"
		date = str(year) + "-" + month + "-01"
		chart = billboard.ChartData(chart_name, date)
		# Checks if track information is already in the file
		for k in range(len(chart)):
			title = chart[k].title.replace(",","|")
			artist = chart[k].artist.replace(",","|")
			track_info = title + "," + artist
			if track_info in tracks_string:
				pass
			else:
				# Otherwise writes in track information
				f.write(track_info + "\n")
				tracks_string = tracks_string + " " + track_info
		time.sleep(5)
	return

# Creates folders and CSV files
def billboard_file_maker(chart_name, start_year, end_year):
	tracks_string = ""
	for year in range(start_year, end_year+1):
		folder_path = os.path.join("Billboard", str(year))
		os.makedirs(folder_path, exist_ok = True)
		filename = get_file_name(chart_name) + " - " + str(year) + ".csv"
		filepath = os.path.join(folder_path, filename)
		if os.path.exists(filepath):
			f = open(filepath,'r')
			tracks_string = f.read()
			f.close()
			f = open(filepath, 'a')
			file_writer(f, chart_name, year, tracks_string)
			f.close()
		else:
			f = open(filepath, 'w')
			header = "Title, Artist\n"
			f.write(header)
			file_writer(f, chart_name, year, tracks_string)
		f.close()

# Input chart name
# Examples: 'hot-mainstream-rock-tracks', 'latin-songs'

billboard_file_maker('latin-songs', 2011,2018)
