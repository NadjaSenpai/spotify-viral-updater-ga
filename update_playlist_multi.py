import csv
import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from playwright.sync_api import sync_playwright

load_dotenv()

def try_download_with_browser(browser_type):
    print(f"🧪 Trying with: {browser_type.name}")
    browser = browser_type.launch(headless=True)
    context = browser.new_context(storage_state="state.json", accept_downloads=True)
    page = context.new_page()

    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        page.goto("https://charts.spotify.com/charts/view/viral-jp-daily/latest", timeout=30000)
        page.wait_for_load_state("domcontentloaded")

        page.evaluate("document.getElementById('onetrust-banner-sdk')?.remove()")

        # ボタンの出現を待機
        page.locator('button[data-encore-id="buttonTertiary"]').first.wait_for(timeout=15000)

        with page.expect_download(timeout=15000) as download_info:
            page.locator('button[data-encore-id="buttonTertiary"]').first.click()


        download = download_info.value
        download.save_as("viral.csv")
        print("✅ CSVダウンロード成功 with", browser_type.name)
        return True

    except Exception as e:
        print(f"❌ {browser_type.name} failed:", e)
        try:
            page.screenshot(path=f"debug_{browser_type.name}.png", full_page=True)
        except:
            pass
        return False

    finally:
        browser.close()

def download_spotify_csv():
    with sync_playwright() as p:
        if not try_download_with_browser(p.chromium):
            print("❌ Chromiumで失敗したので終了します")
        # if try_download_with_browser(p.chromium):
        #     return
        # print("🔁 Chromium失敗 → Firefoxで再試行")
        # if try_download_with_browser(p.firefox):
        #     return
        # print("🛑 Firefoxも失敗 → WebKitで再試行")
        # try_download_with_browser(p.webkit)

def update_playlist():
    if not os.path.exists("viral.csv"):
        print("❌ viral.csv が見つかりません。プレイリスト更新をスキップします。")
        return

    sp = Spotify(auth_manager=SpotifyOAuth(
        scope="playlist-modify-public playlist-modify-private",
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    ))
    playlist_id = os.getenv("SPOTIFY_PLAYLIST_ID")

    results = sp.playlist_items(playlist_id)
    track_uris = [item["track"]["uri"] for item in results["items"]]
    if track_uris:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)
        print(f"🧹 {len(track_uris)} 件のトラックを削除しました")

    with open("viral.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        uris = [row["uri"] for row in reader if row["uri"].startswith("spotify:track:")]
    if uris:
        sp.playlist_add_items(playlist_id, uris)
        print(f"🎵 {len(uris)} 件のトラックをプレイリストに追加しました")

if __name__ == "__main__":
    download_spotify_csv()
    update_playlist()
