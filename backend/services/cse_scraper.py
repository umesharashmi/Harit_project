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
    pdf_url = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def handle_response(response):
            nonlocal pdf_url

            url = response.url
            content_type = response.headers.get("content-type", "")

            if "application/pdf" in content_type or ".pdf" in url.lower():
                pdf_url = url
                print("✅ FOUND PDF:", pdf_url)

        page.on("response", handle_response)

        page.goto(URL, timeout=60000)

        page.wait_for_selector("text=Download", timeout=15000)

        # latest first
        page.locator("text=Download").first.click()

        page.wait_for_timeout(5000)

        browser.close()

    return pdf_url


def download_pdf():
    clean_old_pdfs()

    link = get_latest_pdf()

    if not link:
        print("❌ PDF NOT FOUND")
        return None

    try:
        name = link.split("/")[-1].split("?")[0]
        path = os.path.join(DIR, name)

        r = requests.get(link, timeout=30)
        r.raise_for_status()

        with open(path, "wb") as f:
            f.write(r.content)

        print("✅ DOWNLOADED:", name)
        return path

    except Exception as e:
        print("⚠️ DOWNLOAD ERROR:", e)
        return None


def download_all():
    file_path = download_pdf()

    if not file_path:
        return []

    return [
        {
            "file": file_path,
            "name": file_path.split("/")[-1]
        }
    ]