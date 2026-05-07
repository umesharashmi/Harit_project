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

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(URL, timeout=60000)

        page.wait_for_timeout(5000)

        try:

            # first download button
            link = page.locator("a").filter(has_text="Download").first

            pdf_url = link.get_attribute("href")

            print("RAW URL:", pdf_url)

            if not pdf_url:

                print("❌ PDF URL NOT FOUND")
                return None

            # convert relative -> absolute
            if pdf_url.startswith("/"):

                pdf_url = "https://www.cse.lk" + pdf_url

            print("📄 PDF URL:", pdf_url)

            filename = pdf_url.split("/")[-1]

            filepath = os.path.join(DIR, filename)

            response = requests.get(pdf_url)

            with open(filepath, "wb") as f:

                f.write(response.content)

            print("✅ DOWNLOADED:", filename)

            return filepath

        except Exception as e:

            print("❌ ERROR:", e)

            return None

        finally:

            browser.close()


if __name__ == "__main__":

    clean_old_pdfs()

    print(get_latest_pdf())