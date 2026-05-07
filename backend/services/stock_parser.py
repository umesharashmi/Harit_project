import pdfplumber
import re

from app.database import SessionLocal
from app.models import CorporateDebtMovement


TARGET_HEADER = "Daily Movements on Corporate Debt"


def parse_float(value):

    try:
        return float(str(value).replace(",", "").strip())
    except:
        return 0.0


def parse_int(value):

    try:
        return int(float(str(value).replace(",", "").strip()))
    except:
        return 0


def extract_report_date(text):

    match = re.search(r"(\d{2}\s\w+\s\d{4})", text)

    if match:
        return match.group(1)

    return None


def parse_and_save_corporate_debt(pdf_path):

    db = SessionLocal()

    saved_count = 0

    capture = False

    report_date = None

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if not text:
                    continue

                if not report_date:
                    report_date = extract_report_date(text)

                # start section
                if TARGET_HEADER in text:
                    capture = True

                if capture:

                    tables = page.extract_tables()

                    for table in tables:

                        if not table:
                            continue

                        for row in table:

                            try:

                                row = [
                                    str(cell).replace("\n", " ").strip()
                                    if cell else ""
                                    for cell in row
                                ]

                                # skip invalid rows
                                if len(row) < 13:
                                    continue

                                # skip headers
                                if "Industry" in row[0]:
                                    continue

                                code_id = row[2]

                                # duplicate prevention
                                exists = db.query(
                                    CorporateDebtMovement
                                ).filter(
                                    CorporateDebtMovement.code_id == code_id,
                                    CorporateDebtMovement.report_date == report_date
                                ).first()

                                if exists:
                                    continue

                                item = CorporateDebtMovement(

                                    report_date=report_date,

                                    industry_group=row[0],

                                    company_name=row[1],

                                    code_id=row[2],

                                    debt_date=row[3],

                                    coupon_rate=parse_float(row[4]),

                                    tom=parse_float(row[5]),

                                    spot=parse_float(row[6]),

                                    issued_date=row[7],

                                    maturity_date=row[8],

                                    coupon_freq=parse_int(row[9]),

                                    next_interest_due_date=row[10],

                                    quantity=parse_int(row[11]),

                                    par=parse_float(row[12])
                                )

                                db.add(item)

                                saved_count += 1

                            except Exception as e:

                                print("❌ ROW ERROR:", e)

                # stop section
                if capture and "Top 20 Equity Turnover" in text:
                    break

        db.commit()

        print(f"✅ SAVED {saved_count} RECORDS")

    except Exception as e:

        db.rollback()

        print("❌ PARSER ERROR:", e)

    finally:

        db.close()