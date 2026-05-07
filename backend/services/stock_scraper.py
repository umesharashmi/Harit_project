import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.cse.lk"
URL = BASE + "/publications/cse-daily.component.html"

DIR = "stock_pdfs"


def download_all():
    os.makedirs(DIR, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)

    print("STATUS:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    pdfs = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if ".pdf" in href.lower():

            full = urljoin(BASE, href)

            pdfs.append(full)

    print("FOUND PDFs:", pdfs)

    downloaded = []

    for link in pdfs:

        try:
            filename = link.split("/")[-1]

            path = os.path.join(DIR, filename)

            r = requests.get(link, headers=headers)

            with open(path, "wb") as f:
                f.write(r.content)

            downloaded.append({
                "file": path
            })

            print("DOWNLOADED:", filename)

        except Exception as e:
            print("DOWNLOAD ERROR:", e)

    return downloaded