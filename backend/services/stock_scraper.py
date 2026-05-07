import os
import requests
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

BASE = "https://www.cse.lk"
URL = "https://www.cse.lk/publications/cse-daily"
DIR = "stock_pdfs"


def download_all():

    os.makedirs(DIR, exist_ok=True)

    downloaded = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🌐 Loading page...")

        page.goto(URL, timeout=60000)
        page.wait_for_timeout(5000)

        links = page.locator("a").evaluate_all(
            "els => els.map(e => e.href)"
        )

        pdfs = []

        for link in links:

            if link and ".pdf" in link.lower():

                full = urljoin(BASE, link)

                if full not in pdfs:
                    pdfs.append(full)

        print("📄 PDFs FOUND:", len(pdfs))

        for link in pdfs:

            try:

                filename = link.split("/")[-1]
                path = os.path.join(DIR, filename)

                print("⬇ Downloading:", filename)

                r = requests.get(link, timeout=30)

                if r.status_code == 200:

                    with open(path, "wb") as f:
                        f.write(r.content)

                    downloaded.append({
                        "file": path
                    })

                    print("✅ Saved:", filename)

                else:
                    print("❌ Failed:", r.status_code)

            except Exception as e:
                print("ERROR:", e)

        browser.close()

    return downloaded