from playwright.sync_api import sync_playwright
import requests
import os

URL = "https://www.cse.lk/publications/cse-daily"
DIR = "cse_pdfs"


def get_latest_pdf():
    os.makedirs(DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL, timeout=60000)

        page.wait_for_selector("text=Download")

        try:
            # first Download button
            with page.expect_popup() as popup_info:
                page.get_by_text("Download").first.click()

            popup = popup_info.value

            popup.wait_for_load_state()

            pdf_url = popup.url

            print("PDF URL:", pdf_url)

            filename = pdf_url.split("/")[-1]

            filepath = os.path.join(DIR, filename)

            # download pdf manually
            response = requests.get(pdf_url)

            with open(filepath, "wb") as f:
                f.write(response.content)

            print("✅ DOWNLOADED:", filename)

            browser.close()

            return filepath

        except Exception as e:
            print("❌ Download failed:", str(e))
            browser.close()
            return None