from playwright.sync_api import sync_playwright
import requests
import os

URL = "https://www.cse.lk/publications/cse-daily"
DIR = "cse_pdfs"


def clean_old_pdfs():

    os.makedirs(DIR, exist_ok=True)

    for f in os.listdir(DIR):

        if f.endswith(".pdf"):

            os.remove(os.path.join(DIR, f))

    print("🧹 Old PDFs removed")


def get_latest_pdf():

    os.makedirs(DIR, exist_ok=True)

    found_pdf = None

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        )

        # capture all network responses
        def handle_response(response):

            nonlocal found_pdf

            try:

                url = response.url

                print("🌐 RESPONSE:", url)

                if ".pdf" in url.lower():

                    print("✅ PDF FOUND:", url)

                    found_pdf = url

            except:
                pass

        page.on("response", handle_response)

        try:

            print("🌐 Opening page...")

            page.goto(
                URL,
                timeout=60000,
                wait_until="networkidle"
            )

            # wait extra for JS/API calls
            page.wait_for_timeout(15000)

            # debug screenshot
            page.screenshot(
                path="debug.png",
                full_page=True
            )

            print("📸 Screenshot saved")

            if not found_pdf:

                print("❌ PDF URL NOT FOUND")

                browser.close()

                return None

            pdf_url = found_pdf

            print("📄 PDF URL:", pdf_url)

            filename = pdf_url.split("/")[-1]

            filepath = os.path.join(DIR, filename)

            print("⬇️ Downloading PDF...")

            response = requests.get(
                pdf_url,
                timeout=60,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/122.0.0.0 Safari/537.36"
                    )
                }
            )

            if response.status_code != 200:

                print("❌ Download failed:", response.status_code)

                browser.close()

                return None

            with open(filepath, "wb") as f:

                f.write(response.content)

            print("✅ DOWNLOADED:", filename)

            browser.close()

            return filepath

        except Exception as e:

            print("❌ ERROR:", str(e))

            browser.close()

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

    else:

        print("❌ No PDFs found")

    print("✅ STARTUP TASKS DONE")