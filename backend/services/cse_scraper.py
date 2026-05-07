from playwright.sync_api import sync_playwright
import requests
import os
import re

URL = "https://www.cse.lk/publications/cse-daily"
DIR = "cse_pdfs"


def clean_old_pdfs():

    os.makedirs(DIR, exist_ok=True)

    for f in os.listdir(DIR):

        if f.endswith(".pdf"):

            os.remove(os.path.join(DIR, f))

    print("🧹 Old PDFs removed")


def extract_pdf_url(html):

    matches = re.findall(r'https://[^\s"\']+\.pdf', html)

    if matches:
        return matches[0]

    return None


def get_latest_pdf():

    os.makedirs(DIR, exist_ok=True)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL, timeout=60000)

        page.wait_for_load_state("networkidle")

        try:

            # wait page render
            page.wait_for_timeout(5000)

            html = page.content()

            pdf_url = extract_pdf_url(html)

            if not pdf_url:

                print("❌ PDF URL NOT FOUND")

                browser.close()

                return None

            print("📄 PDF URL:", pdf_url)

            filename = pdf_url.split("/")[-1]

            filepath = os.path.join(DIR, filename)

            response = requests.get(pdf_url, timeout=60)

            if response.status_code != 200:

                print("❌ Download failed:", response.status_code)

                browser.close()

                return None

            with open(filepath, "wb") as f:

                f.write(response.content)

            print("✅ DOWNLOADED:", filename)

            browser.close()

            return filepath

        except Exception as e:

            print("❌ ERROR:", str(e))

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