import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.cse.lk"
URL = "https://www.cse.lk/publications/cse-daily"
DIR = "stock_pdfs"


def download_all():

    os.makedirs(DIR, exist_ok=True)

    downloaded = []

    print("🚀 START SELENIUM SCRAPER")

    # 🔥 headless chrome setup
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        print("🌐 Opening page...")

        driver.get(URL)

        time.sleep(5)  # wait JS load

        html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")

        links = []

        # collect all links
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full = urljoin(BASE, href)
            links.append(full)

        # filter pdfs
        pdfs = list(set([l for l in links if ".pdf" in l.lower()]))

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