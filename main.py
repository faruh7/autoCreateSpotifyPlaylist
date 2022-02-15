import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
client_id_spotify = "04d70cddff9f4dcfa271eefb4d465718"
client_secret = "51a7c6a733df40e19c6944e274f117b1"


year = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{year}/")
data = response.text
soup = BeautifulSoup(data, "html.parser")
still_data = soup.find_all("h3", id="title-of-a-story", class_="c-title")[6::2]
h3_data = still_data[0::2]
song_names = [song.getText().strip("\n") for song in h3_data]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id_spotify,
                                               client_secret=client_secret,
                                               redirect_uri="http://example.com",
                                               scope="user-library-read playlist-modify-private"))

user_id = sp.current_user()["id"]
song_uris = []
year_year = year.split("-")[0]
for i in song_names:
    result = sp.search(q=f"track:{i} year:{year_year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{i} doesn't exist in Spotify. Skipped.")

playlist_name = f"{year} Billboard 100"
my_playlist = sp.user_playlist_create(user_id, name=playlist_name, public=False)
sp.playlist_add_items(playlist_id=my_playlist["id"], items=song_uris)
