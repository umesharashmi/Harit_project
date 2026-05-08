import threading
from app.database import SessionLocal
from app.models import CorporateDebtMovement
from services.cse_scraper import download_all
from services.cse_parser import parse_corporate_debt

# 🔒 prevent multiple runs
_lock = threading.Lock()
_running = False


def process_cse():

    global _running

    if _running:
        print("⚠️ CSE already running - skipping duplicate call")
        return

    with _lock:
        _running = True

        db = SessionLocal()

        try:
            print("🔥 START CSE PROCESS")

            files = download_all()

            if not files:
                print("❌ No PDFs found")
                return

            # clear old data
            db.query(CorporateDebtMovement).delete()
            db.commit()

            counter = 0

            for item in files:

                file_path = item["file"]
                print("📊 PROCESSING:", file_path)

                rows = parse_corporate_debt(file_path)

                for r in rows:

                    try:
                        obj = CorporateDebtMovement(
                            report_date=item["name"],
                            industry_group=r.get("industry_group"),
                            company_name=r.get("company_name"),
                            code_id=r.get("code_id"),
                            debt_date=r.get("debt_date"),
                            coupon_rate=r.get("coupon_rate"),
                            tom=r.get("tom"),
                            spot=r.get("spot"),
                            issued_date=r.get("issued_date"),
                            maturity_date=r.get("maturity_date"),
                            coupon_freq=r.get("coupon_freq"),
                            next_interest_due_date=r.get("next_interest_due_date"),
                            quantity=r.get("quantity"),
                            par=r.get("par")
                        )

                        db.add(obj)
                        counter += 1

                    except Exception as e:
                        print("❌ INSERT ERROR:", e)

            db.commit()

            print("✅ DONE. TOTAL INSERTED:", counter)

        except Exception as e:
            print("💥 PROCESS CRASH:", e)

        finally:
            db.close()
            _running = False