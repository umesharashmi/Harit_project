from playwright.sync_api import sync_playwright
import os

URL = "https://www.cse.lk/publications/cse-daily"

# project root based folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "stocks")


def download_latest_pdf():

    # ✅ auto create folder if not exists
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

        filepath = os.path.join(SAVE_DIR, filename)

        download.save_as(filepath)

        browser.close()

        print("✅ PDF DOWNLOADED:", filepath)

        return filepath