from datetime import datetime, timedelta
import requests
import os

BASE = "https://www.cse.lk/publications/cse-daily/"
DIR = "stock_pdfs"

def get_latest_pdfs():
    pdfs = []
    today = datetime.today()

    for i in range(15):  # increase range
        d = today - timedelta(days=i)

        url = BASE + f"cse_daily_{d.strftime('%Y_%m_%d')}.pdf"

        r = requests.get(url)

        if r.status_code == 200:
            pdfs.append(url)

        if len(pdfs) == 3:
            break

    return pdfs


def download_all():
    os.makedirs(DIR, exist_ok=True)

    links = get_latest_pdfs()

    print("FOUND PDFs:", links)

    files = []

    for url in links:
        name = url.split("/")[-1]
        path = f"{DIR}/{name}"

        if not os.path.exists(path):
            print("⬇️ Downloading:", name)

            r = requests.get(url)

            if r.status_code != 200:
                print("❌ Failed:", url)
                continue

            with open(path, "wb") as f:
                f.write(r.content)

        files.append({"file": path})

    print("FILES:", files)
    return files