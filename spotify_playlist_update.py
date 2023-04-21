# Edited by ChatGPT
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Spotify client information and authentication
spotify_client_id = "your_spotify_client_id"
spotify_client_secret = "your_spotify_client_secret"
redirect_uri = "http://localhost:8888/callback"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret,
    redirect_uri=redirect_uri
))

# Get the current user's Spotify username
sp_user = sp.current_user()
user_name = sp_user['uri'].split(":")[2]

# Set up headers and URL for web scraping
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
url = "https://www.radyoodtu.com.tr/40haramiler"
page = requests.get(url=url, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

# Find artist and song information from the website
div_artist = soup.find_all("div", {"class": "artist"})
div_song = soup.find_all("div", {"class": "song"})

# Remove duplicate songs from the playlist
spotify_playlist_id = "your_playlist_id"
all_songs = sp.playlist_items(playlist_id=spotify_playlist_id)
try:
    set_array = set()
    for i in range(0, 40):
        all_songs_link = all_songs['items'][i]['track']['external_urls']['spotify']
        all_songs_id = str(all_songs_link).split("/")[4]
        set_array.add(str(all_songs_id))
    set_array.discard('')
    sp.playlist_remove_all_occurrences_of_items(playlist_id=spotify_playlist_id, items=set_array)
except KeyError:
    # Handle KeyError exception if playlist has less than 40 songs
    pass

# Add new songs to the playlist
for i in range(0, 40):
    artist_name = div_artist[i+5].text.strip()
    song_name = div_song[i].text.strip()
    song = sp.search(q=artist_name + " " + song_name, type="track")
    song_link = song['tracks']['items'][0]['external_urls']['spotify']
    song_id = str(song_link).split("/")[4]
    sp.playlist_add_items(playlist_id=spotify_playlist_id, items={song_id})