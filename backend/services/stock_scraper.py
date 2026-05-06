import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.cse.lk"
URL = BASE + "/publications/cse-daily"


def get_latest_three_pdfs():
    soup = BeautifulSoup(requests.get(URL).text, "html.parser")

    pdfs = []

    for a in soup.find_all("a"):
        href = a.get("href", "")
        if "cse_daily" in href and href.endswith(".pdf"):
            full = urljoin(BASE, href)
            pdfs.append(full)

    # remove duplicates
    pdfs = list(dict.fromkeys(pdfs))

    return pdfs[:3]   # 🔥 ONLY 3 FILES


def download_all():
    files = []

    for url in get_latest_three_pdfs():
        name = url.split("/")[-1]

        r = requests.get(url)
        if r.status_code != 200:
            continue

        with open(name, "wb") as f:
            f.write(r.content)

        print(f"✅ Downloaded: {name}")

        files.append({
            "file": name
        })

    return files