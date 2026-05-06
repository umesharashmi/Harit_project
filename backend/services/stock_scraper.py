import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://www.cse.lk/publications/cse-daily"
SAVE_DIR = "cse_pdfs"


def get_pdf_links():
    r = requests.get(BASE_URL)

    if r.status_code != 200:
        print("❌ Failed to load page")
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    pdfs = []

    for a in soup.find_all("a", href=True):
        link = a["href"]

        if ".pdf" in link.lower():
            if link.startswith("/"):
                link = "https://www.cse.lk" + link

            pdfs.append(link)

    print("FOUND PDFs:", pdfs[:5])  # preview
    return pdfs[:3]  # latest 3