import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.cse.lk"
URL = BASE + "/publications/cse-daily.component.html"

DIR = "stock_pdfs"


def download_all():

    os.makedirs(DIR, exist_ok=True)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:

        response = requests.get(
            URL,
            headers=headers,
            timeout=30
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print("FAILED TO LOAD PAGE")
            return []

        print("PDF EXISTS:", ".pdf" in response.text.lower())

        soup = BeautifulSoup(response.text, "html.parser")

        pdfs = []

        for a in soup.find_all("a", href=True):

            href = a["href"]

            print("FOUND LINK:", href)

            if ".pdf" in href.lower():

                full_url = urljoin(BASE, href)

                if full_url not in pdfs:
                    pdfs.append(full_url)

        print("FOUND PDFs:", pdfs)

        downloaded = []

        for link in pdfs:

            try:

                filename = link.split("/")[-1]

                path = os.path.join(DIR, filename)

                print("DOWNLOADING:", link)

                pdf_response = requests.get(
                    link,
                    headers=headers,
                    timeout=30
                )

                if pdf_response.status_code == 200:

                    with open(path, "wb") as f:
                        f.write(pdf_response.content)

                    downloaded.append({
                        "file": path
                    })

                    print("DOWNLOADED:", filename)

                else:
                    print(
                        "PDF DOWNLOAD FAILED:",
                        pdf_response.status_code
                    )

            except Exception as e:
                print("DOWNLOAD ERROR:", e)

        return downloaded

    except Exception as e:

        print("SCRAPER ERROR:", e)

        return []