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
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )
        context = browser.new_context()
        page = context.new_page()

        page.goto(URL, timeout=60000)
        page.wait_for_selector("text=Download", timeout=20000)

        download_path = None

        # Try click safely
        with page.expect_popup() as popup_info:
            page.get_by_text("Download").first.click()

        popup = popup_info.value

        # If it opened PDF in new tab
        popup.wait_for_load_state()

        url = popup.url

        if ".pdf" in url.lower():
            import requests

            filename = url.split("/")[-1].split("?")[0]
            download_path = os.path.join(DIR, filename)

            r = requests.get(url, timeout=60)
            r.raise_for_status()

            with open(download_path, "wb") as f:
                f.write(r.content)

            print("✅ DOWNLOADED (via tab):", filename)

        else:
            # fallback: try download event
            popup.close()

            with page.expect_download(timeout=30000) as dl:
                page.get_by_text("Download").first.click()

            download = dl.value
            filename = download.suggested_filename
            download_path = os.path.join(DIR, filename)
            download.save_as(download_path)

            print("✅ DOWNLOADED (via download event):", filename)

        browser.close()
        return download_path


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