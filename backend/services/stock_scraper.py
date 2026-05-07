from playwright.sync_api import sync_playwright
import os
import requests

SAVE_DIR = "pdfs/stocks"
URL = "https://www.cse.lk/publications/cse-daily"

def download_latest_pdf():

    os.makedirs(SAVE_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        links = page.eval_on_selector_all("a", "els => els.map(e => e.href)")

        pdf_url = None
        for link in links:
            if ".pdf" in link:
                pdf_url = link
                break

        browser.close()

    if not pdf_url:
        print("NO PDF FOUND")
        return None

    filename = pdf_url.split("/")[-1]
    path = os.path.join(SAVE_DIR, filename)

    pdf = requests.get(pdf_url)

    with open(path, "wb") as f:
        f.write(pdf.content)

    print("✅ DOWNLOADED:", path)
    return path