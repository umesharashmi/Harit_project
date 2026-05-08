import requests
import os

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
        print("🌐 Fetching API...")

        res = requests.get(URL, headers=headers, timeout=30)
        res.raise_for_status()

        data = res.json()

        # 🔥 DEBUG (uncomment if needed)
        # print(data)

        # ---- SAFE extraction (handles different structures) ----
        pdf_path = None

        if isinstance(data, dict):

            # case 1
            if "data" in data and data["data"]:
                first = data["data"][0]

                if isinstance(first, dict):
                    pdf_path = first.get("file") or first.get("pdf")

            # case 2 fallback
            if not pdf_path:
                for v in data.values():
                    if isinstance(v, list) and v:
                        item = v[0]
                        if isinstance(item, dict):
                            pdf_path = item.get("file") or item.get("pdf")
                            if pdf_path:
                                break

        if not pdf_path:
            print("❌ PDF link not found in API response")
            return None

        # full URL fix
        if pdf_path.startswith("/"):
            pdf_url = "https://www.cse.lk" + pdf_path
        else:
            pdf_url = pdf_path

        print("📄 FINAL PDF URL:", pdf_url)

        filename = pdf_url.split("/")[-1]
        filepath = os.path.join(DIR, filename)

        print("⬇️ Downloading PDF...")

        pdf_res = requests.get(pdf_url, headers=headers, timeout=60)

        if pdf_res.status_code != 200:
            print("❌ Download failed:", pdf_res.status_code)
            return None

        with open(filepath, "wb") as f:
            f.write(pdf_res.content)

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
    print("🔥 START CSE PROCESS")

    result = download_all()

    if result:
        print("✅ DONE")
        print(result)
    else:
        print("❌ No PDFs found")

    print("✅ STARTUP TASKS DONE")