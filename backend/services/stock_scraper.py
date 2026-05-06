from datetime import datetime, timedelta
import requests

BASE_CDN = "https://www.cse.lk/publications/cse-daily/"

def get_latest_three_pdfs():
    pdfs = []
    today = datetime.today()

    for i in range(10):  # check last 10 days
        d = today - timedelta(days=i)

        url = BASE_CDN + f"cse_daily_{d.strftime('%Y_%m_%d')}.pdf"

        r = requests.head(url)

        if r.status_code == 200:
            pdfs.append(url)

        if len(pdfs) == 3:
            break

    print("FOUND PDFs:", pdfs)
    return pdfs


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

        files.append({"file": name})

    return files