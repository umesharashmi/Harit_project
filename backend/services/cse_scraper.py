from playwright.sync_api import sync_playwright
import requests
import os

URL = "https://www.cse.lk/publications/cse-daily"
DIR = "cse_pdfs"


def clean_old_pdfs():
    os.makedirs(DIR, exist_ok=True)

    for f in os.listdir(DIR):
        if f.endswith(".pdf"):
            os.remove(os.path.join(DIR, f))

    print("🧹 Old PDFs removed")


def get_latest_pdf():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)

        # wait for page to load download buttons
        page.wait_for_selector("text=Download", timeout=15000)

        pdf_path = None

        # IMPORTANT FIX: use expect_download (NOT response listener)
        with page.expect_download() as download_info:
            page.get_by_text("Download").first.click()

        download = download_info.value

        # save file
        filename = download.suggested_filename
        pdf_path = os.path.join(DIR, filename)
        download.save_as(pdf_path)

        print("✅ DOWNLOADED:", filename)

        browser.close()

        return pdf_path


def download_pdf():
    clean_old_pdfs()

    file_path = get_latest_pdf()

    if not file_path:
        print("❌ PDF NOT FOUND")
        return None

    return {
        "file": file_path,
        "name": os.path.basename(file_path)
    }


def download_all():
    result = download_pdf()

    if not result:
        return []

    return [result]


if __name__ == "__main__":
    print(download_all())