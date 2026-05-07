from playwright.sync_api import sync_playwright
import os
import requests

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
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

        page = browser.new_page()
        page.goto(URL, timeout=60000)

        page.wait_for_selector("text=Download", timeout=20000)

        # ===== TRY DOWNLOAD EVENT FIRST =====
        try:
            with page.expect_download(timeout=15000) as dl_info:
                page.get_by_text("Download").first.click()

            download = dl_info.value
            filename = download.suggested_filename
            path = os.path.join(DIR, filename)

            download.save_as(path)

            print("✅ DOWNLOADED (event):", filename)
            browser.close()
            return path

        except:
            print("⚠️ Download event failed, trying navigation fallback...")

        # ===== FALLBACK: DIRECT NAVIGATION =====
        with page.expect_navigation(timeout=15000):
            page.get_by_text("Download").first.click()

        url = page.url

        if ".pdf" in url.lower():
            filename = url.split("/")[-1].split("?")[0]
            path = os.path.join(DIR, filename)

            r = requests.get(url, timeout=60)
            r.raise_for_status()

            with open(path, "wb") as f:
                f.write(r.content)

            print("✅ DOWNLOADED (navigation):", filename)
            browser.close()
            return path

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