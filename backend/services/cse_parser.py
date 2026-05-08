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
        return int(str(x).replace(",", "").strip())
    except:
        return None

def parse_equity(file_path):

    rows = []
    inside_section = False

    with pdfplumber.open(file_path) as pdf:

        print("📄 TOTAL PAGES:", len(pdf.pages))

        for page_no, page in enumerate(pdf.pages):

            print(f"🔎 Checking page {page_no+1}")

            text = page.extract_text() or ""

            # ✅ START section
            if "02. Daily Movements on Equity" in text:
                inside_section = True
                print(f"✅ ENTER SECTION (page {page_no+1})")

            # ✅ STOP (FIXED)
            if inside_section and "03." in text and "Debt" in text:
                print(f"⛔ EXIT SECTION (page {page_no+1})")
                break

            if not inside_section:
                continue

            tables = page.extract_tables()

            if not tables:
                continue

            print(f"📊 Page {page_no+1} → Tables: {len(tables)}")

            for table in tables:
                for row in table:

                    if not row:
                        continue

                    row = (row + [None] * 20)[:20]
                    row = [r.strip() if isinstance(r, str) else r for r in row]

                    if row[0] and "Industry" in str(row[0]):
                        continue

                    if all(r is None or r == "" for r in row):
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
                        print(f"❌ ROW ERROR (page {page_no+1}):", e)

    print("✅ TOTAL PARSED ROWS:", len(rows))
    return rows