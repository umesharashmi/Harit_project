import pdfplumber


def clean_float(x):
    try:
        if x is None or x == "":
            return None

        return float(
            str(x)
            .replace(",", "")
            .replace("%", "")
            .strip()
        )

    except:
        return None


def clean_int(x):
    try:
        if x is None or x == "":
            return None

        return int(
            str(x)
            .replace(",", "")
            .strip()
        )

    except:
        return None


def parse_corporate_debt(file_path):

    rows = []

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:

                if not table:
                    continue

                for row in table:

                    if not row:
                        continue

                    # remove empty values
                    row = [r.strip() if isinstance(r, str) else r for r in row]

                    text = " ".join(
                        [str(i) for i in row if i]
                    ).lower()

                    # skip headers
                    if "industry" in text and "company" in text:
                        continue

                    # skip tiny rows
                    if len(row) < 12:
                        continue

                    try:

                        data = {

                            "industry_group":
                                row[0] if len(row) > 0 else None,

                            "company_name":
                                row[1] if len(row) > 1 else None,

                            "code_id":
                                row[2] if len(row) > 2 else None,

                            "debt_date":
                                row[3] if len(row) > 3 else None,

                            "coupon_rate":
                                clean_float(row[4]) if len(row) > 4 else None,

                            "tom":
                                clean_float(row[5]) if len(row) > 5 else None,

                            "spot":
                                clean_float(row[6]) if len(row) > 6 else None,

                            "issued_date":
                                row[7] if len(row) > 7 else None,

                            "maturity_date":
                                row[8] if len(row) > 8 else None,

                            "coupon_freq":
                                clean_int(row[9]) if len(row) > 9 else None,

                            "next_interest_due_date":
                                row[10] if len(row) > 10 else None,

                            "quantity":
                                clean_int(row[11]) if len(row) > 11 else None,

                            "par":
                                clean_float(row[12]) if len(row) > 12 else None,
                        }

                        # skip invalid rows
                        if not data["company_name"]:
                            continue

                        rows.append(data)

                    except Exception as e:
                        print("❌ ROW ERROR:", e)

    print("✅ PARSED ROWS:", len(rows))

    return rows