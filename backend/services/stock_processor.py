from app.database import SessionLocal
from app.models import StockTrade

from services.stock_scraper import download_latest_pdf
from services.stock_parser import parse_stock_pdf


def process_stocks():

    db = SessionLocal()

    print("START STOCK PROCESS")

    pdf_path = download_latest_pdf()

    if not pdf_path:
        return

    rows = parse_stock_pdf(pdf_path)

    print("ROWS:", len(rows))

    for item in rows:

        stock = StockTrade(
            trade_date=item["trade_date"],
            board=item["board"],
            company=item["company"],
            trade_type=item["trade_type"],
            price=item["price"],
            quantity=item["quantity"],
            plus_value=item["plus_value"],
            minus_value=item["minus_value"],
            trades=item["trades"]
        )

        db.add(stock)

    db.commit()

    db.close()

    print("DONE")