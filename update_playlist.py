import csv
import os
import base64
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from playwright.sync_api import sync_playwright

print("🚀 スクリプト起動")

load_dotenv()

def decode_state_json():
    encoded = os.getenv("STATE_JSON_B64")
    if not encoded:
        print("❌ STATE_JSON_B64 が定義されていません")
        return False
    decoded = base64.b64decode(encoded).decode("utf-8")
    with open("state.json", "w", encoding="utf-8") as f:
        f.write(decoded)
    print("✅ state.json を展開しました")
    return True

def download_spotify_csv():
    print("📥 CSV ダウンロード開始")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state="state.json",
            accept_downloads=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="ja-JP",
            timezone_id="Asia/Tokyo",
            geolocation={"longitude": 139.6917, "latitude": 35.6895},
            permissions=["geolocation"]
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        try:
            page.goto("https://charts.spotify.com/charts/view/viral-jp-daily/latest", timeout=30000)
            page.wait_for_load_state("domcontentloaded")
            page.evaluate("document.getElementById('onetrust-banner-sdk')?.remove()")

            page.locator('button[data-encore-id="buttonTertiary"]').first.wait_for(timeout=15000)
            with page.expect_download(timeout=15000) as download_info:
                page.locator('button[data-encore-id="buttonTertiary"]').first.click()

            download = download_info.value
            download.save_as("viral.csv")
            print("✅ CSVダウンロード完了: viral.csv")

        except Exception as e:
            print("❌ CSV ダウンロード失敗:", e)
            try:
                page.screenshot(path="debug.png", full_page=True)
            except:
                pass
        finally:
            browser.close()

def get_spotify_client():
    refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")
    if not refresh_token:
        print("❌ SPOTIFY_REFRESH_TOKEN が未設定です")
        exit(1)

    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    )

    try:
        token_info = auth_manager.refresh_access_token(refresh_token)
        return Spotify(auth=token_info["access_token"])
    except Exception as e:
        print("❌ アクセストークンの取得に失敗しました:", e)
        exit(1)
        
def update_playlist():
    print("🎯 Spotify API 認証処理開始")
    sp = get_spotify_client()

    playlist_id = os.getenv("SPOTIFY_PLAYLIST_ID")
    print("🎧 playlist_id:", playlist_id)

    if not os.path.exists("viral.csv"):
        print("❌ viral.csv が見つかりません")
        return

    # ✅ 既存のトラックを削除
    print("🧹 既存トラックを取得中...")
    results = sp.playlist_items(playlist_id)
    track_uris = [item["track"]["uri"] for item in results["items"] if item["track"]]
    if track_uris:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)
        print(f"🗑️ {len(track_uris)} 件のトラックを削除しました")

    # ✅ 新しいトラックをCSVから読み込んで追加
    with open("viral.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        uris = [row["uri"] for row in reader if row["uri"].startswith("spotify:track:")]
    print("🎵 URI件数:", len(uris))
    if uris:
        sp.playlist_add_items(playlist_id, uris)
        print(f"✅ {len(uris)} 件のトラックをプレイリストに追加しました")

if __name__ == "__main__":
    if decode_state_json():
        download_spotify_csv()
        update_playlist()
