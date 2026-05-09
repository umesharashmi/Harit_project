import pdfplumber


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
        return int(str(x).replace(",", "").strip())   # ✅ FIXED
    except:
        return None


def is_number(val):
    try:
        float(str(val).replace(",", "").replace("%", ""))
        return True
    except:
        return False


def parse_equity(file_path):

    rows = []
    inside_section = False

    with pdfplumber.open(file_path) as pdf:

        print("📄 TOTAL PAGES:", len(pdf.pages))

        for page_no, page in enumerate(pdf.pages):

            text = page.extract_text() or ""

            if "02. Daily Movements on Equity" in text:
                inside_section = True
                print(f"✅ ENTER SECTION (page {page_no+1})")

            if inside_section and "03." in text and "Debt" in text:
                print(f"⛔ EXIT SECTION (page {page_no+1})")
                break

            if not inside_section:
                continue

            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:
                for row in table:

                    if not row:
                        continue

                    # clean row
                    row = [
                        r.replace("\n", " ").strip() if isinstance(r, str) else r
                        for r in row
                    ]

                    # remove empty cells
                    row = [r for r in row if r not in (None, "")]

                    # skip short rows
                    if len(row) < 10:
                        continue

                    # skip headers
                    if "Industry" in str(row[0]):
                        continue

                    # ensure numeric columns
                    if not is_number(row[-1]) or not is_number(row[-2]):
                        continue

                    try:
                        data = {
                            "industry_group": row[0],
                            "board": row[1] if len(row) > 1 else None,
                            "company_name": row[2] if len(row) > 2 else None,
                            "type": row[3] if len(row) > 3 else None,
                            "close_price": clean_float(row[4]) if len(row) > 4 else None,
                            "last_traded_price": clean_float(row[5]) if len(row) > 5 else None,
                            "last_traded_date": row[6] if len(row) > 6 else None,
                            "high": clean_float(row[7]) if len(row) > 7 else None,
                            "low": clean_float(row[8]) if len(row) > 8 else None,
                            "foreign_holding": clean_int(row[9]) if len(row) > 9 else None,
                            "turnover": clean_float(row[10]) if len(row) > 10 else None,
                            "quantity": clean_int(row[11]) if len(row) > 11 else None,
                        }

                        rows.append(data)

                    except Exception as e:
                        print(f"❌ ROW ERROR (page {page_no+1}):", e)

    print("✅ TOTAL PARSED ROWS:", len(rows))
    return rows