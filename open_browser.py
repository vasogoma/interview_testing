from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headed mode
    page = browser.new_page()
    page.goto("https://app.enshift.com/forgot-password")

    print("Browser is open. Press Enter in console to close it.")
    input()  # wait for user input to keep browser open

    browser.close()
