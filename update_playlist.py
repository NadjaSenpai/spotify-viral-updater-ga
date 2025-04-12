import csv
import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from playwright.sync_api import sync_playwright

load_dotenv()

def download_spotify_csv():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()
        page.goto("https://charts.spotify.com/charts/view/viral-jp-daily/latest", timeout=180000)

        # 安定したセレクタ + 長めのタイムアウト
        page.wait_for_selector('button[data-encore-id="buttonTertiary"] >> nth=0', timeout=120000)

        with page.expect_download() as download_info:
            page.click('button[data-encore-id="buttonTertiary"] >> nth=0')
        download = download_info.value
        download.save_as("viral.csv")
        browser.close()

def update_playlist():
    sp = Spotify(auth_manager=SpotifyOAuth(
        scope="playlist-modify-public playlist-modify-private",
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    ))
    playlist_id = os.getenv("SPOTIFY_PLAYLIST_ID")

    # 全トラック削除
    results = sp.playlist_items(playlist_id)
    track_uris = [item["track"]["uri"] for item in results["items"]]
    if track_uris:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)

    # 新しいトラック追加
    with open("viral.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        uris = [row["uri"] for row in reader if row["uri"].startswith("spotify:track:")]
    if uris:
        sp.playlist_add_items(playlist_id, uris)

if __name__ == "__main__":
    download_spotify_csv()
    update_playlist()
