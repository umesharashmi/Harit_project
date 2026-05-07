import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.cse.lk"
URL = BASE + "/publications/cse-daily"

SAVE_DIR = "pdfs/stocks"


def download_latest_pdf():

    os.makedirs(SAVE_DIR, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)

    print(response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.text)

    pdf_url = None

    for a in soup.find_all("a", href=True):

        href = a["href"]

        print(href)

        if ".pdf" in href.lower():

            pdf_url = urljoin(BASE, href)
            break

    if not pdf_url:

        print("NO PDF FOUND")
        return None

    filename = pdf_url.split("/")[-1]

    path = os.path.join(SAVE_DIR, filename)

    pdf = requests.get(pdf_url, headers=headers)

    with open(path, "wb") as f:
        f.write(pdf.content)

    print("✅ DOWNLOADED:", path)

    return path