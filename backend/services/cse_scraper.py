from playwright.sync_api import sync_playwright
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
    os.makedirs(DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)
        page.wait_for_selector("text=Download", timeout=30000)

        try:
            # ONLY THIS METHOD
            with page.expect_download(timeout=30000) as dl_info:
                page.get_by_text("Download").first.click()

            download = dl_info.value
            filename = download.suggested_filename
            path = os.path.join(DIR, filename)

            download.save_as(path)

            print("✅ DOWNLOADED:", filename)

            browser.close()
            return path

        except Exception as e:
            print("❌ Download failed:", str(e))
            browser.close()
            return None


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
    return [result] if result else []


if __name__ == "__main__":
    print(download_all())