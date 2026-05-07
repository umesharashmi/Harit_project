from playwright.sync_api import sync_playwright
import os

URL = "https://www.cse.lk/publications/cse-daily"


def download_latest_pdf():

    # 🔥 auto detect project root
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # 🔥 auto create folder inside project
    SAVE_DIR = os.path.join(BASE_DIR, "stocks")

    os.makedirs(SAVE_DIR, exist_ok=True)

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        page = browser.new_page()

        page.goto(URL)
        page.wait_for_load_state("networkidle")

        with page.expect_download() as download_info:
            page.locator("text=Download").first.click()

        download = download_info.value

        filename = download.suggested_filename

        # 🔥 auto safe file path
        filepath = os.path.join(SAVE_DIR, filename)

        download.save_as(filepath)

        browser.close()

        print("✅ PDF DOWNLOADED:", filepath)

        return filepath