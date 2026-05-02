from services.scraper import download_all
from services.parser import parse_pdf
from app.database import SessionLocal
from app.models import Price

def process_all():
    db = SessionLocal()

    print("PROCESS STARTED")

    # 🔥 Clear DB
    db.query(Price).delete()
    db.commit()

    files = download_all()
    print("FILES:", files)

    counter = 0  # global counter (avoid duplicate IDs)

    for f in files:
        rows = parse_pdf(f)
        print("ROWS COUNT:", len(rows))

        for r in rows:
            try:
                # unique ID
                uid = f"{r.get('date')}_{r.get('city')}_{r.get('item')}_{counter}"
                counter += 1

                print("INSERTING:", uid)

                #  safe insert (NO **r)
                new_price = Price(
                    id=uid,
                    date=r.get("date"),
                    city=r.get("city"),
                    item=r.get("item"),
                    category=r.get("category"),
                    min_price=r.get("min_price"),
                    max_price=r.get("max_price")
                )

                db.add(new_price)
                db.commit()   #  commit per row

            except Exception as e:
                import traceback
                print("ERROR INSERTING:", uid)
                traceback.print_exc()
                db.rollback()

    db.close()
    print("PROCESS COMPLETED")

