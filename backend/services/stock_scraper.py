import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.cse.lk"
URL = BASE + "/publications/cse-daily"

SAVE_DIR = "pdfs/stocks"


def download_latest_pdf():

    os.makedirs(SAVE_DIR, exist_ok=True)

    soup = BeautifulSoup(requests.get(URL).text, "html.parser")

    pdf_url = None

    for a in soup.find_all("a"):

        href = a.get("href", "")

        if ".pdf" in href:

            pdf_url = urljoin(BASE, href)
            break

    if not pdf_url:
        print("No PDF found")
        return None

    filename = pdf_url.split("/")[-1]

    path = os.path.join(SAVE_DIR, filename)

    response = requests.get(pdf_url)

    with open(path, "wb") as f:
        f.write(response.content)

    print("Downloaded:", path)

    return path