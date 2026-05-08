from app.database import SessionLocal
from app.models import CorporateDebtMovement
from services.cse_scraper import download_all
from services.cse_parser import parse_corporate_debt


def process_cse():

    db = SessionLocal()

    print("🔥 START CSE PROCESS")

    files = download_all()

    if not files:
        print("❌ No PDFs found")
        return

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

                    industry_group=r["industry_group"],
                    company_name=r["company_name"],
                    code_id=r["code_id"],
                    debt_date=r["debt_date"],
                    coupon_rate=r["coupon_rate"],
                    tom=r["tom"],
                    spot=r["spot"],
                    issued_date=r["issued_date"],
                    maturity_date=r["maturity_date"],
                    coupon_freq=r["coupon_freq"],
                    next_interest_due_date=r["next_interest_due_date"],
                    quantity=r["quantity"],
                    par=r["par"]

                )

                db.add(obj)
                counter += 1

            except Exception as e:
                print("❌ INSERT ERROR:", e)

    db.commit()
    db.close()

    print("✅ DONE. TOTAL INSERTED:", counter)