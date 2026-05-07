from playwright.sync_api import sync_playwright
import os

URL = "https://www.cse.lk/publications/cse-daily"


def clean_old_pdfs(folder):

    if os.path.exists(folder):

        for file in os.listdir(folder):

            file_path = os.path.join(folder, file)

            if os.path.isfile(file_path):

                os.remove(file_path)

                print("🗑️ DELETED OLD FILE:", file_path)


def download_latest_pdf():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SAVE_DIR = os.path.join(BASE_DIR, "stocks")

    os.makedirs(SAVE_DIR, exist_ok=True)

    # 🔥 STEP 1: delete old PDFs first
    clean_old_pdfs(SAVE_DIR)

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

        print("✅ NEW PDF DOWNLOADED:", filepath)

        return filepath