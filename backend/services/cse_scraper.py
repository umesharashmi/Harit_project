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


def get_latest_3_pdfs():

    os.makedirs(DIR, exist_ok=True)

    files = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🌐 Opening page...")

        page.goto(URL, timeout=60000)
        page.wait_for_load_state("networkidle")

        # 🔥 GET ALL DOWNLOAD BUTTONS
        buttons = page.locator("button:has-text('Download'), a:has-text('Download')")
        count = buttons.count()

        print("🔎 TOTAL DOWNLOADS FOUND:", count)

        for i in range(min(3, count)):

            with page.expect_download() as download_info:
                buttons.nth(i).click()

            download = download_info.value

            filepath = os.path.join(DIR, download.suggested_filename)
            download.save_as(filepath)

            print(f"⬇️ DOWNLOADED {i+1}:", filepath)

            files.append(filepath)

        browser.close()

    return files


def download_all():

    clean_old_pdfs()

    file_paths = get_latest_3_pdfs()

    results = []

    for i, path in enumerate(file_paths):

        clean_name = f"cse_{time.strftime('%Y%m%d')}_{i}.pdf"
        new_path = os.path.join(DIR, clean_name)

        os.rename(path, new_path)

        results.append({
            "file": new_path,
            "name": clean_name
        })

    return results