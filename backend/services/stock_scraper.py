import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.cse.lk"
URL = "https://www.cse.lk/publications/cse-daily"
DIR = "stock_pdfs"


def download_all():

    os.makedirs(DIR, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    downloaded = []

    try:
        print("🌐 Loading page...")

        r = requests.get(URL, headers=headers, timeout=30)

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            print("FAILED TO LOAD PAGE")
            return []

        soup = BeautifulSoup(r.text, "html.parser")

        links = []

        # collect all possible links
        for a in soup.find_all("a", href=True):

            href = a["href"]

            if href:
                links.append(urljoin(BASE, href))

        pdfs = []

        for link in links:

            if ".pdf" in link.lower():

                if link not in pdfs:
                    pdfs.append(link)

        print("📄 PDFs FOUND:", len(pdfs))

        for link in pdfs:

            try:

                filename = link.split("/")[-1]
                path = os.path.join(DIR, filename)

                print("⬇ Downloading:", filename)

                pdf = requests.get(link, headers=headers, timeout=30)

                if pdf.status_code == 200:

                    with open(path, "wb") as f:
                        f.write(pdf.content)

                    downloaded.append({"file": path})

                    print("✅ Saved:", filename)

                else:
                    print("❌ PDF FAIL:", pdf.status_code)

            except Exception as e:
                print("ERROR:", e)

        return downloaded

    except Exception as e:
        print("SCRAPER ERROR:", e)
        return []