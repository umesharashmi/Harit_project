import pdfplumber
import re
from datetime import datetime


def parse_stock_pdf(pdf_path):

    rows = []

    with pdfplumber.open(pdf_path) as pdf:

        full_text = ""

        for page in pdf.pages:
            full_text += page.extract_text() + "\n"

    # date extract
    date_match = re.search(r"(\d{2} \w+ \d{4})", full_text)

    trade_date = None

    if date_match:
        trade_date = datetime.strptime(
            date_match.group(1),
            "%d %B %Y"
        ).date()

    lines = full_text.split("\n")

    capture = False

    for line in lines:

        # stock section start
        if "Share Prices and Trends" in line:
            capture = True
            continue

        if not capture:
            continue

        parts = line.split()

        # skip invalid rows
        if len(parts) < 8:
            continue

        try:

            board = parts[0]

            # company name detect
            company = " ".join(parts[1:-6])

            trade_type = parts[-6]

            price = float(parts[-5].replace(",", ""))

            quantity = int(parts[-4].replace(",", ""))

            plus_value = float(parts[-3])

            minus_value = float(parts[-2])

            trades = int(parts[-1])

            rows.append({
                "trade_date": trade_date,
                "board": board,
                "company": company,
                "trade_type": trade_type,
                "price": price,
                "quantity": quantity,
                "plus_value": plus_value,
                "minus_value": minus_value,
                "trades": trades
            })

        except:
            pass

    return rows