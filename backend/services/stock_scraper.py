import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.cse.lk"
URL = BASE + "/publications/cse-daily"


def get_latest_three_pdfs():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    pdfs = []

    # 🔥 grab ALL pdf links
    for a in soup.find_all("a", href=True):
        href = a["href"]

        # only pdf files
        if ".pdf" in href:
            full = urljoin(BASE, href)
            pdfs.append(full)

    # remove duplicates
    pdfs = list(dict.fromkeys(pdfs))

    print("FOUND PDFs:", pdfs)

    return pdfs[:3]   # latest 3


def download_all():
    files = []

    urls = get_latest_three_pdfs()

    if not urls:
        print("❌ No PDFs found")
        return files

    for url in urls:
        name = url.split("/")[-1]

        r = requests.get(url)

        if r.status_code != 200:
            print("❌ Failed:", url)
            continue

        with open(name, "wb") as f:
            f.write(r.content)

        print(f"✅ Downloaded: {name}")

        files.append({
            "file": name
        })

    return files