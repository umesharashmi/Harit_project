import os
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


SAVE_DIR = "pdfs/stocks"

URL = "https://www.cse.lk/publications/cse-daily"


def download_latest_pdf():

    os.makedirs(SAVE_DIR, exist_ok=True)

    options = webdriver.ChromeOptions()

    options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL)

    time.sleep(5)

    links = driver.find_elements(By.TAG_NAME, "a")

    pdf_url = None

    for link in links:

        href = link.get_attribute("href")

        print(href)

        if href and ".pdf" in href.lower():

            pdf_url = href
            break

    driver.quit()

    if not pdf_url:

        print("NO PDF FOUND")
        return None

    filename = pdf_url.split("/")[-1]

    path = os.path.join(SAVE_DIR, filename)

    response = requests.get(pdf_url)

    with open(path, "wb") as f:
        f.write(response.content)

    print("✅ DOWNLOADED:", path)

    return path