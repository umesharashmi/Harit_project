from playwright.sync_api import sync_playwright
import requests
import os

URL = "https://www.cse.lk/publications/cse-daily"
DIR = "cse_pdfs"


# ✅ 1. delete only old PDFs (keep folder)
def clean_old_pdfs():
    os.makedirs(DIR, exist_ok=True)

    for file in os.listdir(DIR):
        if file.lower().endswith(".pdf"):
            os.remove(os.path.join(DIR, file))

    print("🧹 Old PDF files removed (folder kept)")


# ✅ 2. get PDF links (FINAL FIX)
def get_pdf_links():
    pdf_links = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)

        # wait until content loads
        page.wait_for_timeout(5000)

        # 🔥 get all hrefs
        links = page.eval_on_selector_all(
            "a",
            "els => els.map(e => e.href)"
        )

        for link in links:
            if link and ".pdf" in link.lower():
                pdf_links.append(link)

        browser.close()

    # remove duplicates
    pdf_links = list(set(pdf_links))

    # sort latest first
    pdf_links.sort(reverse=True)

    return pdf_links[:1]   # 🔥 latest PDF only (06 May 2026)


# ✅ 3. download PDFs
def download_all():
    clean_old_pdfs()

    files = []

    links = get_pdf_links()
    print("📄 FOUND LINKS:", links)

    if not links:
        print("❌ No PDF links found")
        return files

    for link in links:
        try:
            name = link.split("/")[-1].split("?")[0]
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


