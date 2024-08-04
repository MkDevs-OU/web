from playwright.sync_api import sync_playwright

def test_status_code():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        response = page.goto('https://www.mkdevs.ee')
        assert response.status == 200, f"Expected status code 200 but got {response.status}"
        browser.close()
