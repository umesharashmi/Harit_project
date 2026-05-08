import requests
import os
import re
from urllib.parse import urljoin

URL = "https://www.cse.lk/publications/cse-daily"
BASE_URL = "https://www.cse.lk"
DIR = "cse_pdfs"


def clean_old_pdfs():

    os.makedirs(DIR, exist_ok=True)

    for f in os.listdir(DIR):

        if f.lower().endswith(".pdf"):

            try:
                os.remove(os.path.join(DIR, f))
            except Exception:
                pass

    print("🧹 Old PDFs removed")


def extract_pdf_url(html):

    # Absolute PDF links
    patterns = [

        r'https?:\/\/[^\s"\']+\.pdf',

        r'\/[^\s"\']+\.pdf'
    ]

    for pattern in patterns:

        match = re.search(pattern, html, re.IGNORECASE)

        if match:

            pdf_url = match.group(0)

            return urljoin(BASE_URL, pdf_url)

    return None


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

        response = requests.get(
            URL,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        html = response.text

        print("🔍 Searching PDF link...")

        pdf_url = extract_pdf_url(html)

        if not pdf_url:

            print("❌ No PDF URL found")
            return None

        print("📄 PDF URL FOUND:")
        print(pdf_url)

        filename = pdf_url.split("/")[-1]

        # remove query params
        filename = filename.split("?")[0]

        filepath = os.path.join(DIR, filename)

        print("⬇️ Downloading PDF...")

        pdf_response = requests.get(
            pdf_url,
            headers=headers,
            timeout=60
        )

        pdf_response.raise_for_status()

        content_type = pdf_response.headers.get(
            "Content-Type",
            ""
        )

        # optional validation
        if "pdf" not in content_type.lower():

            print("⚠️ Warning: Response may not be PDF")
            print("Content-Type:", content_type)

        with open(filepath, "wb") as f:

            f.write(pdf_response.content)

        print("✅ PDF DOWNLOADED SUCCESSFULLY")
        print("📁 Saved to:", filepath)

        return filepath

    except requests.exceptions.RequestException as e:

        print("❌ NETWORK ERROR:")
        print(str(e))

        return None

    except Exception as e:

        print("❌ ERROR:")
        print(str(e))

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

    if result:
        return [result]

    return []


if __name__ == "__main__":

    print("🔥 START CSE PROCESS\n")

    result = download_all()

    print()

    if result:

        print("✅ DONE")
        print(result)

    else:

        print("❌ No PDFs found")

    print("\n✅ STARTUP TASKS DONE")