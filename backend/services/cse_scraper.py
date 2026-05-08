from playwright.sync_api import sync_playwright
import requests
import os
from urllib.parse import urljoin

URL = "https://www.cse.lk/publications/cse-daily"
BASE_URL = "https://www.cse.lk"
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

    try:

        print("🌐 Opening browser...")

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            page.goto(URL, timeout=60000)

            # wait page render
            page.wait_for_timeout(5000)

            print("🔍 Searching download links...")

            links = page.locator("a").evaluate_all(
                """
                elements => elements.map(el => el.href)
                """
            )

            browser.close()

        pdf_url = None

        for link in links:

            if ".pdf" in link.lower():

                pdf_url = link
                break

        if not pdf_url:

            print("❌ PDF URL not found")
            return None

        pdf_url = urljoin(BASE_URL, pdf_url)

        print("📄 PDF URL:")
        print(pdf_url)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        print("⬇️ Downloading PDF...")

        response = requests.get(
            pdf_url,
            headers=headers,
            timeout=60
        )

        response.raise_for_status()

        filename = pdf_url.split("/")[-1]
        filename = filename.split("?")[0]

        filepath = os.path.join(DIR, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        print("✅ DOWNLOADED:", filename)

        return filepath

    except Exception as e:

        print("❌ ERROR:", str(e))
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

    print("🔥 START CSE PROCESS\n")

    result = download_all()

    print()

    if result:

        print("✅ DONE")
        print(result)

    else:

        print("❌ No PDFs found")

    print("\n✅ STARTUP TASKS DONE")