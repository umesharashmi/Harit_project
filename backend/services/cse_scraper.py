from playwright.sync_api import sync_playwright
import requests
import os

URL = "https://www.cse.lk/publications/cse-daily"
DIR = "cse_pdfs"


# ✅ 1. delete only old PDF files (NOT folder)
def clean_old_pdfs():
    os.makedirs(DIR, exist_ok=True)

    for file in os.listdir(DIR):
        if file.endswith(".pdf"):
            os.remove(os.path.join(DIR, file))

    print("🧹 Old PDF files removed (folder kept)")


# ✅ 2. get PDF links using button click (FIXED)
def get_pdf_links():
    pdf_links = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)

        # wait until buttons load
        page.wait_for_selector("text=Download", timeout=15000)

        buttons = page.locator("text=Download")
        count = buttons.count()

        print("🔘 DOWNLOAD BUTTONS FOUND:", count)

        for i in range(count):
            try:
                # click and capture new tab
                with page.expect_popup() as popup_info:
                    buttons.nth(i).click()

                new_page = popup_info.value
                new_page.wait_for_load_state()

                pdf_url = new_page.url

                if ".pdf" in pdf_url:
                    pdf_links.append(pdf_url)
                    print("✅ PDF LINK:", pdf_url)

                new_page.close()

            except Exception as e:
                print("⚠️ CLICK ERROR:", e)

        browser.close()

    # remove duplicates
    pdf_links = list(set(pdf_links))

    # sort latest first (optional)
    pdf_links.sort(reverse=True)

    return pdf_links[:2]  # latest 2


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
            name = link.split("/")[-1].split("?")[0]  # clean filename
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