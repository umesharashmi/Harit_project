from services.stock_scraper import download_latest_pdf

from services.stock_parser import parse_and_save_corporate_debt


def process_stocks():

    try:

        print("📥 DOWNLOADING PDF...")

        pdf_path = download_latest_pdf()

        if not pdf_path:

            print("❌ DOWNLOAD FAILED")

            return

        print("📄 PARSING PDF...")

        parse_and_save_corporate_debt(pdf_path)

        print("✅ STOCK PROCESS COMPLETED")

    except Exception as e:

        print("❌ STOCK PROCESS ERROR:", e)