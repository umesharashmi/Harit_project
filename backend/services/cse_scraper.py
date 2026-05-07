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

    os.makedirs(DIR, exist_ok=True)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL, timeout=60000)

        page.wait_for_load_state("networkidle")

        try:

            # FIRST DOWNLOAD BUTTON
            btn = page.locator("a:has-text('Download')").first

            # GET PDF URL
            href = btn.get_attribute("href")

            if not href:
                print("❌ No href found")
                browser.close()
                return None

            # HANDLE RELATIVE URL
            if href.startswith("/"):

                pdf_url = "https://www.cse.lk" + href

            else:

                pdf_url = href

            print("📄 PDF URL:", pdf_url)

            # FILE NAME
            filename = pdf_url.split("/")[-1]

            if not filename.endswith(".pdf"):

                filename = "latest_cse_daily.pdf"

            filepath = os.path.join(DIR, filename)

            # DOWNLOAD PDF
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