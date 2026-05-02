import pdfplumber


def clean_number(x):
    try:
        if x is None:
            return None
        return int(str(x).replace(",", "").replace("*", "").strip())
    except:
        return None


def is_country(cell):
    """
    Detect country name:
    - string
    - no digits
    """
    return (
        isinstance(cell, str)
        and cell.strip() != ""
        and not any(char.isdigit() for char in cell)
    )


def parse_country_pdf(file):
    rows = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:

            tables = page.extract_tables()

            for table in tables:
                for row in table:

                    if not row:
                        continue

                    # skip header
                    if "country" in str(row).lower():
                        continue

                    try:
                        # find country dynamically
                        country = None
                        for cell in row:
                            if is_country(cell):
                                country = cell.strip()
                                break

                        if not country:
                            continue

                        # extract numeric values only
                        nums = []
                        for cell in row:
                            num = clean_number(cell)
                            if num is not None:
                                nums.append(num)

                        # need at least rank + 1 month
                        if len(nums) < 2:
                            continue

                        #  remove rank (first number always rank)
                        nums = nums[1:]

                        # last value = total
                        total = nums[-1]

                        # months = everything except total
                        months_data = nums[:-1]

                        #  dynamically map months
                        month_keys = [
                            "jan","feb","mar","apr","may","jun",
                            "jul","aug","sep","oct","nov","dec"
                        ]

                        data = {"country": country}

                        for i in range(12):
                            if i < len(months_data):
                                data[month_keys[i]] = months_data[i]
                            else:
                                data[month_keys[i]] = 0

                        data["total"] = total

                        rows.append(data)

                    except Exception as e:
                        print("ROW ERROR:", e)

    print("✅ FINAL ROW COUNT:", len(rows))
    return rows