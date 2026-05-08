from playwright.sync_api import sync_playwright
import os

URL = "https://www.cse.lk/publications/cse-daily"
BASE_URL = "https://www.cse.lk"
DIR = "cse_pdfs"


def clean_old_pdfs():

    os.makedirs(DIR, exist_ok=True)

    for f in os.listdir(DIR):

        if f.lower().endswith(".pdf"):

            try:
                os.remove(os.path.join(DIR, f))
            except:
                pass

    print("🧹 Old PDFs removed")


def get_latest_pdf():

    os.makedirs(DIR, exist_ok=True)

    try:

        print("🌐 Opening browser...")

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            context = browser.new_context(
                accept_downloads=True
            )

            page = context.new_page()

            page.goto(
                URL,
                timeout=60000
            )

            # wait fully loaded
            page.wait_for_timeout(8000)

            print("🔍 Searching download button...")

            # all buttons / links
            buttons = page.locator("a, button")

            count = buttons.count()

            print(f"TOTAL BUTTONS/LINKS: {count}")

            download_button = None

            for i in range(count):

                try:

                    text = buttons.nth(i).inner_text().strip()

                    print(f"{i} -> {text}")

                    if "download" in text.lower():

                        download_button = buttons.nth(i)
                        break

                except:
                    pass

            if not download_button:

                print("❌ Download button not found")

                browser.close()

                return None

            print("⬇️ Clicking download button...")

            with page.expect_download() as download_info:

                download_button.click()

            download = download_info.value

            filename = download.suggested_filename

            filepath = os.path.join(
                DIR,
                filename
            )

            download.save_as(filepath)

            browser.close()

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

    print("🔥 START CSE PROCESS\n")

    result = download_all()

    print()

    if result:

        print("✅ DONE")
        print(result)

    else:

        print("❌ No PDFs found")

    print("\n✅ STARTUP TASKS DONE")