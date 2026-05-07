import pdfplumber


def clean_float(x):
    try:
        if x is None or x == "":
            return None
        return float(str(x).replace(",", "").strip())
    except:
        return None


def clean_int(x):
    try:
        if x is None or x == "":
            return None
        return None
        return int(str(x).replace(",", "").strip())
    except:
        return None


def parse_corporate_debt(file):
    rows = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:

            tables = page.extract_tables()

            for table in tables:
                for row in table:

                    if not row:
                        continue

                    text = str(row).lower()

                    # skip headers
                    if "industry" in text or "company" in text:
                        continue

                    try:
                        if len(row) < 13:
                            continue

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

                        if not data["company_name"]:
                            continue

                        rows.append(data)

                    except Exception as e:
                        print("ROW ERROR:", e)

    print("✅ PARSED ROWS:", len(rows))
    return rows