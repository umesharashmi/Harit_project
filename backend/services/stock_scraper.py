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

    soup = BeautifulSoup(response.text, "html.parser")

    pdf_links = []

    for a in soup.find_all("a"):

        href = a.get("href", "")

        if ".pdf" in href.lower():

            full_url = urljoin(BASE, href)

            pdf_links.append(full_url)

    print("PDF LINKS:", pdf_links)

    if not pdf_links:

        print("No PDF found")
        return None

    # latest pdf
    pdf_url = pdf_links[0]

    filename = pdf_url.split("/")[-1]

    path = os.path.join(SAVE_DIR, filename)

    pdf = requests.get(pdf_url, headers=headers)

    with open(path, "wb") as f:
        f.write(pdf.content)

    print("Downloaded:", path)

    return path