import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.cse.lk/publications/cse-daily"
DIR = "cse_pdfs"


def clean_old_pdfs():
    os.makedirs(DIR, exist_ok=True)

    for f in os.listdir(DIR):
        if f.endswith(".pdf"):
            try:
                os.remove(os.path.join(DIR, f))
            except:
                pass

    print("🧹 Old PDFs removed")


def get_latest_pdf():

    os.makedirs(DIR, exist_ok=True)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    try:

        print("🌐 Opening CSE page...")

        res = requests.get(URL, headers=headers, timeout=30)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        # Find ALL links
        links = soup.find_all("a", href=True)

        pdf_url = None

        for link in links:

            href = link["href"]

            # detect pdf
            if ".pdf" in href.lower():

                pdf_url = urljoin("https://www.cse.lk", href)
                break

        if not pdf_url:
            print("❌ No PDF URL found")
            return None

        print("📄 PDF URL:", pdf_url)

        filename = pdf_url.split("/")[-1]
        filepath = os.path.join(DIR, filename)

        print("⬇️ Downloading PDF...")

        pdf_res = requests.get(pdf_url, headers=headers, timeout=60)
        pdf_res.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(pdf_res.content)

        print("✅ DOWNLOADED:", filename)

        return filepath

    except Exception as e:
        print("❌ ERROR:", str(e))
        return None


def download_pdf():

    clean_old_pdfs()

    file_path = get_latest_pdf()

    if not file_path:
        print("❌ PDF NOT FOUND")
        return None

    return {
        "file": file_path,
        "name": os.path.basename(file_path)
    }


def download_all():

    result = download_pdf()

    return [result] if result else []


if __name__ == "__main__":

    print("🔥 START CSE PROCESS")

    result = download_all()

    if result:
        print("✅ DONE")
        print(result)
    else:
        print("❌ No PDFs found")

    print("✅ STARTUP TASKS DONE")