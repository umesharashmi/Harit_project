import requests, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.cse.lk"
URL = BASE + "/pages/cse-daily/cse-daily.component.html"
DIR = "stock_pdfs"


def download_all():
    os.makedirs(DIR, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []

    # 🔍 find PDF links
    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "cse_daily" in href and href.endswith(".pdf"):
            full_url = urljoin(BASE, href)
            links.append(full_url)

    # ✅ take latest 3 (like your requirement)
    links = links[:3]

    print("FOUND PDFs:", links)

    files = []

    for url in links:
        name = url.split("/")[-1]
        path = f"{DIR}/{name}"

        if not os.path.exists(path):
            print("⬇️ Downloading:", name)

            r = requests.get(url, headers=headers)

            if r.status_code != 200:
                print("❌ Failed:", url)
                continue

            with open(path, "wb") as f:
                f.write(r.content)

        files.append({"file": path})

    # 🧹 delete old files (same as your HARTI logic)
    for f in os.listdir(DIR):
        full = f"{DIR}/{f}"
        if not any(full == item["file"] for item in files):
            os.remove(full)

    print("FILES:", files)

    return files