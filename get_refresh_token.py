import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# .envを読み込む
load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")  # http://127.0.0.1:8888/callback を使用
SCOPE = "playlist-modify-public playlist-modify-private"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=".spotify_token_cache"
)

auth_url = sp_oauth.get_authorize_url()
print("↓↓↓ このURLをブラウザで開いてログインしてください ↓↓↓\n")
print(auth_url)
print("\n↑↑↑ ログイン後にリダイレクトされたURLをコピーして貼り付けてください ↑↑↑\n")

# 入力待ち
redirect_response = input("リダイレクトされたURLを貼り付けてください:\n")

# アクセストークン取得
code = sp_oauth.parse_response_code(redirect_response)
token_info = sp_oauth.get_access_token(code)

print("\n✅ Access Token:", token_info['access_token'])
print("✅ Refresh Token:", token_info['refresh_token'])
