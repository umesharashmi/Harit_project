import requests
import os

DIR = "stock_pdfs"
API_URL = "https://www.cse.lk/api/cse-publications"


def download_all():

    os.makedirs(DIR, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(API_URL, headers=headers, timeout=30)

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            print("API FAILED")
            return []

        data = r.json()

        # 🔥 SAFE CHECK (important)
        if isinstance(data, dict):
            data = data.get("data", [])

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

                pdf = requests.get(full_url, headers=headers, timeout=30)

                if pdf.status_code != 200:
                    print("PDF FAIL:", full_url)
                    continue

                with open(path, "wb") as f:
                    f.write(pdf.content)

                downloaded.append({
                    "file": path
                })

                print("DOWNLOADED:", filename)

            except Exception as e:
                print("ITEM ERROR:", e)

        return downloaded

    except Exception as e:
        print("REQUEST ERROR:", e)
        return []