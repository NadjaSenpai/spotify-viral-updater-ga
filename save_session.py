from playwright.sync_api import sync_playwright
import base64

def save_login_state_and_encode():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://charts.spotify.com")

        print("✅ ログインして 'ダウンロード' ボタンが表示されるまで、手動で操作してね")
        input("ログイン完了後にEnterを押して続行...")

        context.storage_state(path="state.json")
        browser.close()
        print("✅ ログインセッションを state.json に保存しました")

        # base64 エンコードして出力
        with open("state.json", "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            print("\n👇 以下を GitHub の Secrets（STATE_JSON）に登録してください：\n")
            print(encoded)

if __name__ == "__main__":
    save_login_state_and_encode()
