from playwright.sync_api import sync_playwright

def save_login_state():
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

if __name__ == "__main__":
    save_login_state()
