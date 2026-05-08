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


def parse_corporate_debt(file_path):

    rows = []
    inside_section = False

    with pdfplumber.open(file_path) as pdf:

        print("📄 TOTAL PAGES:", len(pdf.pages))

        for page_no, page in enumerate(pdf.pages, start=1):

            text = page.extract_text()

            # ✅ START section detect
            if text and "02. Daily Movements on Corporate Debt" in text:
                inside_section = True
                print(f"✅ ENTER SECTION (page {page_no})")

            # ✅ STOP when next section comes
            if inside_section and text and "03." in text:
                print(f"⛔ EXIT SECTION (page {page_no})")
                break

            if not inside_section:
                continue

            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:

                if not table:
                    continue

                for row in table:

                    if not row:
                        continue

                    # normalize length (important for broken rows)
                    row = (row + [None] * 20)[:20]

                    # clean spaces
                    row = [r.strip() if isinstance(r, str) else r for r in row]

                    # ❌ skip header rows
                    if row[0] and "Industry" in str(row[0]):
                        continue

                    # ❌ skip fully empty rows
                    if all(r is None or r == "" for r in row):
                        continue

                    # ⚠️ DO NOT SKIP PARTIAL DATA (keep original requirement)
                    try:
                        data = {
                            "industry_group": row[0],
                            "company_name": row[1],
                            "code_id": row[2],
                            "debt_date": row[3],
                            "coupon_rate": clean_float(row[4]),
                            "tom": clean_float(row[5]),
                            "spot": clean_float(row[6]),
                            "issued_date": row[7],
                            "maturity_date": row[8],
                            "coupon_freq": clean_int(row[9]),
                            "next_interest_due_date": row[10],
                            "quantity": clean_int(row[11]),
                            "par": clean_float(row[12]),
                        }

                        rows.append(data)

                    except Exception as e:
                        print(f"❌ ROW ERROR (page {page_no}):", e)

    print("✅ TOTAL PARSED ROWS:", len(rows))
    return rows