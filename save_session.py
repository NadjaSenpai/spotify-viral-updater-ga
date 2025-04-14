from playwright.sync_api import sync_playwright
import base64

def save_login_state_and_encode():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://charts.spotify.com")

        print("Log in manually and wait for the 'Download' button to appear.")
        input("Press Enter after login is complete...")

        context.storage_state(path="state.json")
        browser.close()
        print("Saved session to state.json")

        with open("state.json", "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            print("\nCopy the following and add it to your secrets as STATE_JSON_B64:\n")
            print(encoded)

if __name__ == "__main__":
    save_login_state_and_encode()