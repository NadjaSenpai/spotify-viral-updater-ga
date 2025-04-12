import csv
import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from playwright.sync_api import sync_playwright

load_dotenv()

def download_spotify_csv():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(storage_state="state.json", accept_downloads=True)
        page = context.new_page()

        # webdriverステルス対策
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        try:
            page.goto("https://charts.spotify.com/charts/view/viral-jp-daily/latest", timeout=60000)
            page.evaluate("document.getElementById('onetrust-banner-sdk')?.remove()")

            # ダウンロードボタン出現待ち
            page.locator('button[data-encore-id="buttonTertiary"]').first.wait_for(timeout=15000)
            with page.expect_download() as download_info:
                page.locator('button[data-encore-id="buttonTertiary"]').first.click()

            download = download_info.value
            download.save_as("viral.csv")
            print("✅ CSVダウンロード完了: viral.csv")

        except Exception as e:
            print("❌ ダウンロード失敗:", e)
            page.screenshot(path="debug.png", full_page=True)
            raise
        finally:
            browser.close()

def update_playlist():
    sp = Spotify(auth_manager=SpotifyOAuth(
        scope="playlist-modify-public playlist-modify-private",
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    ))
    playlist_id = os.getenv("SPOTIFY_PLAYLIST_ID")

    # 既存トラックを全削除
    results = sp.playlist_items(playlist_id)
    track_uris = [item["track"]["uri"] for item in results["items"]]
    if track_uris:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)
        print(f"🧹 {len(track_uris)} 件のトラックを削除しました")

    # CSVから新しいトラックを読み込み
    with open("viral.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        uris = [row["uri"] for row in reader if row["uri"].startswith("spotify:track:")]
    if uris:
        sp.playlist_add_items(playlist_id, uris)
        print(f"🎵 {len(uris)} 件のトラックをプレイリストに追加しました")

if __name__ == "__main__":
    download_spotify_csv()
    update_playlist()
