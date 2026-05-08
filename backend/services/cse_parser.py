import pdfplumber
import re

def clean_text(x):
    if x is None:
        return ""
    return " ".join(str(x).split())

def clean_float(x):
    try:
        if x is None or x == "":
            return None
        return float(str(x).replace(",", "").replace("%", "").strip())
    except:
        return None

def clean_int(x):
    try:
        if x is None or x == "":
            return None
        return int(str(x).replace(",", "").strip())
    except:
        return None


def parse_equity(file_path):

    rows = []
    inside_section = False

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            text = page.extract_text() or ""

            # ✅ better section detection
            if "02. Daily Movements on Equity" in text:
                inside_section = True

            if inside_section and "03." in text and "Debt" in text:
                break

            if not inside_section:
                continue

            tables = page.extract_tables() or []

            for table in tables:
                for row in table:

                    if not row:
                        continue

                    # ✅ normalize row (important fix)
                    row = [(clean_text(r)) for r in row if r is not None]

                    # skip header
                    if len(row) > 0 and "Industry" in row[0]:
                        continue

                    # ❌ skip broken rows
                    if len(row) < 12:
                        continue

                    try:
                        data = {
                            "industry_group": row[0],
                            "board": row[1],
                            "company_name": row[2],
                            "type": row[3],
                            "close_price": clean_float(row[4]),
                            "last_traded_price": clean_float(row[5]),
                            "last_traded_date": row[6],
                            "high": clean_float(row[7]),
                            "low": clean_float(row[8]),
                            "foreign_holding": clean_int(row[9]),
                            "turnover": clean_float(row[10]),
                            "quantity": clean_int(row[11]),
                        }

                        rows.append(data)

                    except Exception as e:
                        print("ROW ERROR:", e)

    print("TOTAL ROWS:", len(rows))
