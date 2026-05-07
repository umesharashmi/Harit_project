import os
import requests
from bs4 import BeautifulSoup

SAVE_DIR = "pdfs/stocks"

URL = "https://www.cse.lk/publications/cse-daily"


def download_latest_pdf():

    os.makedirs(SAVE_DIR, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(URL, headers=headers)

    if res.status_code != 200:
        print("REQUEST FAILED:", res.status_code)
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    pdf_url = None

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if ".pdf" in href.lower():
            pdf_url = requests.compat.urljoin(URL, href)
            break

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