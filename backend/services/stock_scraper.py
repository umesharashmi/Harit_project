import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin

BASE = "https://www.cse.lk"
URL = "https://www.cse.lk/publications/cse-daily"
DIR = "stock_pdfs"


def download_all():

    os.makedirs(DIR, exist_ok=True)

    downloaded = []

    print("🚀 START SELENIUM SCRAPER")

    # 🔥 Chrome setup (IMPORTANT FIXED)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)

    try:

        print("🌐 Opening page...")

        driver.get(URL)

        # better than fixed sleep
        time.sleep(8)

        # full rendered HTML
        html = driver.page_source

        pdfs = []

        # extract PDF links directly (better logic)
        for line in html.split('"'):

            if ".pdf" in line.lower():

                full = urljoin(BASE, line)

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

                    downloaded.append({"file": path})

                    print("✅ Saved:", filename)

                else:
                    print("❌ FAIL:", r.status_code)

            except Exception as e:
                print("ERROR:", e)

        return downloaded

    except Exception as e:
        print("SCRAPER ERROR:", e)
        return []

    finally:
        driver.quit()