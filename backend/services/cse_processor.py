import threading
from app.database import SessionLocal
from app.models import EquityMovement
from services.cse_scraper import download_all
from services.cse_parser import parse_equity

def process_cse():

    db = SessionLocal()

    try:
        print("🔥 START CSE PROCESS")

        files = download_all()

        if not files:
            print("❌ No PDFs found")
            return

        print("🧹 Clearing old data...")
        db.query(EquityMovement).delete()
        db.commit()

        counter = 0

        for item in files:

            file_path = item["file"]
            print("📊 PROCESSING:", file_path)

            rows = parse_equity(file_path)

            if not rows:
                print("⚠️ No rows parsed")
                return

            for r in rows:
                try:
                    obj = EquityMovement(
                        report_date=item["name"],
                        industry_group=r.get("industry_group"),
                        board=r.get("board"),
                        company_name=r.get("company_name"),
                        type=r.get("type"),
                        close_price=r.get("close_price"),
                        last_traded_price=r.get("last_traded_price"),
                        last_traded_date=r.get("last_traded_date"),
                        high=r.get("high"),
                        low=r.get("low"),
                        foreign_holding=r.get("foreign_holding"),
                        turnover=r.get("turnover"),
                        quantity=r.get("quantity"),
                    )

                    db.add(obj)
                    counter += 1

                    if counter % 100 == 0:
                        db.commit()
                        print(f"💾 committed {counter}")

                except Exception as e:
                    print("❌ INSERT ERROR:", e)
                    db.rollback()   # 🔥 VERY IMPORTANT FIX

        db.commit()
        print("✅ DONE. TOTAL INSERTED:", counter)

    except Exception as e:
        print("💥 PROCESS CRASH:", e)

    finally:
        db.close()