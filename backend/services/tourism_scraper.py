import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re

BASE = "https://www.sltda.gov.lk"
URL = BASE + "/en/tourist-arrivals-from-all-countries"

DIR = "tourism_pdfs"


def extract_year(url):
    match = re.search(r"(20\d{2})", url)
    return int(match.group(1)) if match else 0


def get_latest_two_pdfs():
    soup = BeautifulSoup(requests.get(URL).text, "html.parser")

    pdfs = []

    for a in soup.find_all("a"):
        href = a.get("href", "")
        if ".pdf" in href.lower():
            full = urljoin(BASE, href)
            year = extract_year(full)
            pdfs.append((full, year))

    pdfs = sorted(pdfs, key=lambda x: x[1], reverse=True)

    return pdfs[:2]


def download_all():
    os.makedirs(DIR, exist_ok=True)

    files = []

    for url, year in get_latest_two_pdfs():

        name = url.split("/")[-1]
        path = f"{DIR}/{name}"

        r = requests.get(url)
        if r.status_code != 200:
            continue

        with open(path, "wb") as f:
            f.write(r.content)

        print(f"✅ Downloaded: {name} | YEAR: {year}")

        files.append({
            "file": path,
            "year": year
        })

    return files