import requests, os
from bs4 import BeautifulSoup

BASE = "https://www.harti.gov.lk/daily-price.php"
DIR = "pdfs"

def download_all():
    os.makedirs(DIR, exist_ok=True)

    soup = BeautifulSoup(requests.get(BASE).text, "html.parser")

    links = []
    for a in soup.find_all("a"):
        if a.get("href") and ".pdf" in a.get("href"):
            links.append("https://www.harti.gov.lk/" + a.get("href"))

    links = links[:7]

    files = []

    for url in links:
        name = url.split("/")[-1]
        path = f"{DIR}/{name}"

        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(requests.get(url).content)

        files.append(path)

    # delete old
    for f in os.listdir(DIR):
        full = f"{DIR}/{f}"
        if full not in files:
            os.remove(full)

    return files


