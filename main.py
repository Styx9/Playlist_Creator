import requests
from bs4 import BeautifulSoup
import  spotipy
from flask.cli import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
load_dotenv()
date = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD  ")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/120.0.0.0'}
base_url = "https://www.billboard.com/charts/hot-100/"
response = requests.get(base_url + date, headers=headers)
response.raise_for_status()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="https://example.com",
    scope="playlist-modify-private"
))
user = sp.current_user()
# print("Your Spotify username (id) is:", user["id"])
data = response.text
soup = BeautifulSoup(data, 'html.parser')
song_titles = []
# song_artists = []
song_uris = []
for row in soup.select("ul.o-chart-results-list-row"):
    title = row.select_one("h3#title-of-a-story")
    song_titles.append(title.get_text(strip=True) if title else None)
    # artist = row.select_one("h3#title-of-a-story + span.c-label")
    # artist = song_artists.append(artist.get_text(strip=True) if artist else None)
# print(song_titles[:10])
for i in range(len(song_titles)):
    try:
        response = sp.search(q=f"track:{song_titles[i]} year:{date[0:4]}", type="track", limit=1)
        tracks = response["tracks"]["items"]
        if tracks:
            song_uri = tracks[0]["uri"]
            song_uris.append(song_uri)
        else:
            print(f"No results for {song_titles[i]}")
    except Exception as e:
        print(f"Error: {e}")
# print(len(song_uris))
playlist_resp = sp.user_playlist_create(user = user["id"],name = f"{date} Billboard Top Tracks", public=False,description=f"{date} Billboard Top Tracks")
playlist_id = playlist_resp["id"]
add_songs_resp = sp.playlist_add_items(playlist_id,song_uris)