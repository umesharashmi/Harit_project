from playwright.sync_api import sync_playwright
import os
import time

URL = "https://www.cse.lk/publications/cse-daily"
DIR = "cse_pdfs"


def clean_old_pdfs():
    os.makedirs(DIR, exist_ok=True)

    for f in os.listdir(DIR):
        if f.lower().endswith(".pdf"):
            try:
                os.remove(os.path.join(DIR, f))
            except:
                pass

    print("🧹 Old PDFs removed")


def get_latest_pdf():

    os.makedirs(DIR, exist_ok=True)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("🌐 Opening browser...")

        page.goto(URL, timeout=60000)
        page.wait_for_load_state("networkidle")

        print("🔍 Searching download button...")

        # 🔥 FIX ONLY: more stable locator (NO logic change)
        download_button = page.locator("button:has-text('Download'), a:has-text('Download')").first

        if download_button.count() == 0:
            print("❌ Download button not found")
            return None

        print("⬇️ Clicking download...")

        with page.expect_download() as download_info:
            download_button.click(force=True)

        download = download_info.value

        filepath = os.path.join(DIR, download.suggested_filename)
        download.save_as(filepath)

        browser.close()

        print("✅ DOWNLOADED:", filepath)

        return filepath


def download_all():

    clean_old_pdfs()

    files = get_latest_pdfs(3)   # 🔥 ONLY CHANGE

    if not files:
        return []

    results = []

    for i, file_path in enumerate(files):

        clean_name = f"cse_{time.strftime('%Y%m%d')}_{i}.pdf"
        new_path = os.path.join(DIR, clean_name)

        os.rename(file_path, new_path)

        results.append({
            "file": new_path,
            "name": clean_name
        })

    return results