import pdfplumber
import uuid
from datetime import datetime


def parse_stock_pdf(file):
    results = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:

            text = page.extract_text()

            if "Share Prices and Trends" not in text:
                continue

            # extract date
            date = None
            for line in text.split("\n"):
                if "/" in line:
                    try:
                        date = datetime.strptime(line.strip(), "%m/%d/%Y").date()
                        break
                    except:
                        continue

            if not date:
                date = datetime.today().date()

            tables = page.extract_tables()

            for table in tables:
                if not table:
                    continue

                if "Company Name" not in table[0]:
                    continue

                for row in table[1:]:
                    try:
                        results.append({
                            "id": str(uuid.uuid4()),
                            "date": date,
                            "board": row[0],
                            "company": row[1],
                            "type": row[2],
                            "price": float(row[3]),
                            "quantity": int(str(row[4]).replace(",", "")),
                            "gain": float(row[5]) if row[5] else 0,
                            "loss": float(row[6]) if row[6] else 0,
                            "trades": int(row[7])
                        })
                    except:
                        continue

    return results