from app.database import SessionLocal
from app.models import CountryArrival

from services.tourism_scraper import download_all
from services.tourism_parser import parse_country_pdf


def process_country():
    db = SessionLocal()

    print("🔥 START PROCESS")

    files = download_all()

    # clear old data
    db.query(CountryArrival).delete()
    db.commit()

    counter = 0

    for item in files:

        file_path = item["file"]
        year = item["year"]

        rows = parse_country_pdf(file_path)

        print(f"YEAR {year} → ROWS:", len(rows))

        for r in rows:
            try:

                # ✅ SKIP TOTAL ROW (IMPORTANT FIX)
                country_name = r["country"].strip().lower()

                if "total" in country_name:
                    continue

                obj = CountryArrival(
                    id=f"{r['country']}_{counter}_{year}",
                    country=r["country"],
                    year=year,
                    jan=r["jan"],
                    feb=r["feb"],
                    mar=r["mar"],
                    apr=r["apr"],
                    may=r["may"],
                    jun=r["jun"],
                    jul=r["jul"],
                    aug=r["aug"],
                    sep=r["sep"],
                    oct=r["oct"],
                    nov=r["nov"],
                    dec=r["dec"],
                    total=r["total"]
                )

                db.add(obj)
                counter += 1

            except Exception as e:
                print("ERROR:", e)

    db.commit()
    db.close()

    print("✅ DONE")