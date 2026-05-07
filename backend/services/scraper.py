import requests
import os

DIR = "stock_pdfs"

API_URL = "https://www.cse.lk/api/cse-publications"

def download_all():

    os.makedirs(DIR, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(API_URL, headers=headers)

    print("STATUS:", r.status_code)

    data = r.json()

    downloaded = []

    for item in data:

        try:

            file_url = item.get("file")

            if not file_url:
                continue

            if ".pdf" not in file_url.lower():
                continue

            full_url = "https://www.cse.lk" + file_url

            filename = full_url.split("/")[-1]

            path = os.path.join(DIR, filename)

            pdf = requests.get(full_url, headers=headers)

            with open(path, "wb") as f:
                f.write(pdf.content)

            downloaded.append({
                "file": path
            })

            print("DOWNLOADED:", filename)

        except Exception as e:
            print("ERROR:", e)

    return downloaded