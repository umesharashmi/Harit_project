import os
import requests

SAVE_DIR = "pdfs/stocks"

# ⚡ (Most cases CSE uses backend JSON endpoint like this pattern)
API_URL = "https://www.cse.lk/api/publications/cse-daily"


def download_latest_pdf_api():

    os.makedirs(SAVE_DIR, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    res = requests.get(API_URL, headers=headers)

    if res.status_code != 200:
        print("API ERROR:", res.status_code)
        return None

    data = res.json()

    # 🔍 assume API returns list of files
    pdf_url = None

    for item in data.get("data", []):
        file_url = item.get("fileUrl") or item.get("url")

        if file_url and file_url.lower().endswith(".pdf"):
            pdf_url = file_url
            break

    if not pdf_url:
        print("NO PDF FOUND FROM API")
        return None

    filename = pdf_url.split("/")[-1]
    path = os.path.join(SAVE_DIR, filename)

    pdf = requests.get(pdf_url)

    with open(path, "wb") as f:
        f.write(pdf.content)

    print("✅ DOWNLOADED:", path)

    return path