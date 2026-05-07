from playwright.sync_api import sync_playwright
import requests
import os
import re

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


def extract_pdf_from_html(html):

    try:

        matches = re.findall(
            r'https://[^\s"\']+\.pdf',
            html,
            re.IGNORECASE
        )

        if matches:

            print("✅ PDF FOUND IN HTML")

            return matches[0]

        return None

    except Exception as e:

        print("❌ HTML EXTRACT ERROR:", str(e))

        return None


def get_latest_pdf():

    os.makedirs(DIR, exist_ok=True)

    found_pdf = None

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context(
            viewport={
                "width": 1920,
                "height": 1080
            },
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        )

        page = context.new_page()

        # capture network responses
        def handle_response(response):

            nonlocal found_pdf

            try:

                url = response.url

                print("🌐 RESPONSE:", url)

                if ".pdf" in url.lower():

                    print("✅ PDF FOUND IN NETWORK:", url)

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

            # wait for JS rendering
            page.wait_for_timeout(15000)

            # save screenshot
            page.screenshot(
                path="debug.png",
                full_page=True
            )

            print("📸 Screenshot saved")

            # get html
            html = page.content()

            # try html extract
            if not found_pdf:

                found_pdf = extract_pdf_from_html(html)

            # fallback: check all links
            if not found_pdf:

                print("🔍 Checking all links...")

                links = page.locator("a")

                count = links.count()

                print("🔗 TOTAL LINKS:", count)

                for i in range(count):

                    try:

                        href = links.nth(i).get_attribute("href")

                        text = links.nth(i).inner_text().strip()

                        print(f"{i} | TEXT: {text} | HREF: {href}")

                        if href and ".pdf" in href.lower():

                            if href.startswith("/"):

                                href = "https://www.cse.lk" + href

                            found_pdf = href

                            print("✅ PDF FOUND IN LINKS:", found_pdf)

                            break

                    except:
                        pass

            if not found_pdf:

                print("❌ PDF URL NOT FOUND")

                browser.close()

                return None

            print("📄 FINAL PDF URL:", found_pdf)

            filename = found_pdf.split("/")[-1]

            filepath = os.path.join(DIR, filename)

            print("⬇️ Downloading PDF...")

            response = requests.get(
                found_pdf,
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

        print(result)

    else:

        print("❌ No PDFs found")

    print("✅ STARTUP TASKS DONE")