#!/usr/bin/python3
import requests
import csv
import sys

# Set default query argument if none is passed
if len(sys.argv) < 2:
    query = "car"
else:
    query = sys.argv[1]

# Create an empty list to store the song data
song_data = []

for page_number in range(1,2):
   # Musixmatch API endpoint and parameters
   endpoint = "https://api.musixmatch.com/ws/1.1/track.search"
   params = {
       "q_lyrics": query,
       "f_has_lyrics": 1,
       "f_lang_code": "en", ### Hardcoded english language
       "f_track_release_group_first_release_date_max":"2010101", ## Hardcoded release date of song
       "page_size": 20, ## Hardcode page size - so as not to overload API
       "page": page_number,
       "apikey": "3621259dea6ab9eabdeb5dca97728d1b" ## Hardcoded API key 
   }

   # Send the API request and get the JSON response
   response = requests.get(endpoint, params=params).json()
   
   # Iterate through the tracks in the response
   for track in response["message"]["body"]["track_list"]:
       # Get the song data
       track_name = track["track"]["track_name"]
       artist_name = track["track"]["artist_name"]
       album_name = track["track"]["album_name"]
       track_share_url = track["track"]["track_share_url"]
       try:
           album_id = track["track"]["album_id"]

           # Get the album release date
           endpoint2 = "https://api.musixmatch.com/ws/1.1/album.get"
           params2 = {
              "album_id": album_id,
              "apikey": "3621259dea6ab9eabdeb5dca97728d1b"
           }
           response2 = requests.get(endpoint2, params=params2).json()
           album_details=response2["message"]["body"]["album"]
           album_release_date = album_details["album_release_date"]
           if album_release_date < "2010-01-01":
               # Add the song data to the list
               song_data.append([track_name, artist_name, album_name, track_share_url])
       except:
           pass

# Write the song data to a CSV file
filename="songs_with_"+query+".csv"
with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Track name", "Artist Name", "Album name","Track Share URL"])
    writer.writerows(song_data)
print(f"{len(song_data)} song(s) found and saved to",filename)

