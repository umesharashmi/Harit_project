from playwright.sync_api import sync_playwright
import requests
import os

URL = "https://www.cse.lk/publications/cse-daily"
BASE = "https://www.cse.lk"
DIR = "cse_pdfs"


# ✅ delete only old PDF files (NOT folder)
def clean_old_pdfs():
    os.makedirs(DIR, exist_ok=True)

    for file in os.listdir(DIR):
        if file.endswith(".pdf"):
            os.remove(os.path.join(DIR, file))

    print("🧹 Old PDF files removed (folder kept)")


# ✅ get PDF links (JS site)
def get_pdf_links():
    pdf_links = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)
        page.wait_for_timeout(5000)

        anchors = page.locator("a")
        count = anchors.count()

        for i in range(count):
            href = anchors.nth(i).get_attribute("href")

            if href and ".pdf" in href.lower():
                if href.startswith("/"):
                    href = BASE + href

                pdf_links.append(href)

        browser.close()

    # remove duplicates
    pdf_links = list(set(pdf_links))

    return pdf_links[:2]  # latest 2


# ✅ download PDFs
def download_all():
    clean_old_pdfs()  # 🔥 only delete PDFs inside folder

    files = []

    links = get_pdf_links()
    print("📄 FOUND LINKS:", links)

    if not links:
        print("❌ No PDF links found")
        return files

    for link in links:
        try:
            name = link.split("/")[-1]
            path = os.path.join(DIR, name)

            r = requests.get(link)

            if r.status_code != 200:
                print("❌ Failed:", link)
                continue

            with open(path, "wb") as f:
                f.write(r.content)

            print(f"✅ Downloaded: {name}")

            files.append({
                "file": path,
                "name": name
            })

        except Exception as e:
            print("⚠️ DOWNLOAD ERROR:", e)

    return files