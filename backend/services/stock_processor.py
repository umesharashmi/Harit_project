from app.database import SessionLocal
from app.models import Stock

from services.stock_scraper import download_all
from services.stock_parser import parse_stock_pdf


def process_stocks():
    db = SessionLocal()

    print("🔥 STOCK PROCESS START")

    files = download_all()

    counter = 0

    for item in files:
        file_path = item["file"]

        rows = parse_stock_pdf(file_path)

        print(f"{file_path} → ROWS:", len(rows))

        for r in rows:
            try:
                exists = db.query(Stock).filter(
                    Stock.company == r["company"],
                    Stock.date == r["date"]
                ).first()

                if exists:
                    continue

                obj = Stock(**r)

                db.add(obj)
                counter += 1

            except Exception as e:
                print("ERROR:", e)

    db.commit()
    db.close()

    print("✅ STOCK DONE:", counter)