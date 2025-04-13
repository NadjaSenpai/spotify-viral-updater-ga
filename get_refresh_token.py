import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-modify-public playlist-modify-private"
)

auth_url = sp_oauth.get_authorize_url()
print("🔗 下記URLで認証してください:\n", auth_url)

response = input("🔑 リダイレクト先URLを貼ってください: ")

code = sp_oauth.parse_response_code(response)
token_info = sp_oauth.get_access_token(code)
print("✅ refresh_token:", token_info["refresh_token"])
