from bs4 import BeautifulSoup
import requests
from pprint import pprint
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URL = os.environ.get("SPOTIPY_REDIRECT_URI")
USER_AGENT = os.environ.get("USER_AGENT")

date = input("Which year do you want to travel to? "
             "Type the date in this format YYYY-MM-DD: ")

year = date[:4]


billboard_url = "https://www.billboard.com/charts/hot-100/"
header = {
    "User-Agent": USER_AGENT
}

response = requests.get(url=f"{billboard_url}{date}/", headers= header)
response.raise_for_status()
data = response.text

soup = BeautifulSoup(data, "html.parser")
song_title = soup.find_all(name="h3", class_="u-line-height-22px")

song_list=[]
for songs in song_title:
    music = songs.get_text()
    formatted_music = music.strip()
    song_list.append(formatted_music)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URL,
    scope="playlist-modify-private"
))

sp_id = sp.current_user()["id"]

result = []
for song in song_list:
    searched = sp.search(q=f"track:{song}", type="track", limit=1)
    try:
        uri =searched["tracks"]["items"][0]["uri"]
        result.append(uri)
    except IndexError:
        print(f"❌ Track not found on Spotify: {song}")

playlist = sp.user_playlist_create(user=sp_id,
                        name=f"{date} Billboard 100",
                        public=False,
                        description= "The top 100 songs from a certain date!")

playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=result)

print("Playlist created successfully✅")

spotify = spotipy.oauth2.SpotifyOAuth()


