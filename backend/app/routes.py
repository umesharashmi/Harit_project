from fastapi import APIRouter, HTTPException
from sqlalchemy import func
from .database import SessionLocal
from .models import Price
from services.parser import parse_pdf
from datetime import datetime

router = APIRouter()


@router.get("/prices")
def get_all_prices(
    item: str = None,
    category: str = None,
    city: str = None,
    start: str = None,
    end: str = None
):
    db = SessionLocal()

    try:
        query = db.query(Price)

        # 🔥 FILTERS
        if item:
            query = query.filter(Price.item == item)

        if category:
            query = query.filter(Price.category == category)

        if city:
            query = query.filter(Price.city == city)

        if start and end:
            start = start.replace("-", ".")
            end = end.replace("-", ".")
            query = query.filter(Price.date >= start, Price.date <= end)

        data = query.all()

        return [
            {
                "date": d.date,
                "item": d.item,
                "category": d.category,
                "city": d.city,
                "min_price": d.min_price,
                "max_price": d.max_price
            }
            for d in data
        ]

    finally:
        db.close()
        
@router.get("/filters")
def filters():
    db = SessionLocal()

    try:
        return {
            "dates": [d[0] for d in db.query(Price.date).distinct()],
            "items": [
                {"name": i[0], "category": i[1]}
                for i in db.query(Price.item, Price.category).distinct()
            ],
            "categories": [c[0] for c in db.query(Price.category).distinct()],
            "cities": [c[0] for c in db.query(Price.city).distinct()],
        }
    finally:
        db.close()

@router.get("/load")
def load_data():
    db = SessionLocal()

    try:
        import os

        # 🔥 backend folder
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 🔥 pdf folder
        pdf_folder = os.path.join(BASE_DIR, "pdfs")

        #  check folder
        if not os.path.exists(pdf_folder):
            return {"error": f"PDF folder not found: {pdf_folder}"}

        # =========================
        # 🔥 CLEAR OLD DATA FIRST
        # =========================
        deleted = db.query(Price).delete()
        db.commit()

        print(f"OLD DATA CLEARED: {deleted} rows")

        # =========================
        # 🔥 LOAD NEW DATA
        # =========================
        pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

        total = 0

        for pdf in pdf_files:
            file_path = os.path.join(pdf_folder, pdf)

            data = parse_pdf(file_path)

            print(f"{pdf} → {len(data)} rows")

            for d in data:
                db.add(Price(**d))

            total += len(data)

        db.commit()

        return {
            "message": f"{total} new rows inserted",
            "old_rows_deleted": deleted
        }

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()


# ✅ SINGLE DATE AVG
@router.get("/avg")
def average(date: str = None, item: str = None, category: str = None, city: str = None):
    db = SessionLocal()
    try:
        query = db.query(func.avg((Price.min_price + Price.max_price) / 2))

        if date:
            query = query.filter(Price.date == date)

        if item:
            query = query.filter(Price.item == item)

        if category:
            query = query.filter(Price.category == category)

        if city:
            query = query.filter(Price.city == city)

        avg = query.scalar()

        return {"average": float(avg) if avg else 0}

    finally:
        db.close()


# ✅ RANGE AVG (🔥 FIXED SAFE VERSION)
@router.get("/avg-range")
def avg_range(start: str, end: str, item: str = None, category: str = None, city: str = None):
    db = SessionLocal()

    try:
        # convert dash → dot
        start = start.replace("-", ".")
        end = end.replace("-", ".")

        # swap if wrong
        if start > end:
            start, end = end, start

        # 🔥 OVERALL AVERAGE
        query = db.query(func.avg((Price.min_price + Price.max_price) / 2))
        query = query.filter(Price.date >= start, Price.date <= end)

        if item:
            query = query.filter(Price.item == item)
        if category:
            query = query.filter(Price.category == category)
        if city:
            query = query.filter(Price.city == city)

        avg = query.scalar()

        # 🔥 DAILY DATA (THIS WAS MISSING ❗)
        data_query = db.query(
            Price.date,
            func.avg((Price.min_price + Price.max_price) / 2).label("average")
        ).filter(
            Price.date >= start,
            Price.date <= end
        )

        if item:
            data_query = data_query.filter(Price.item == item)
        if category:
            data_query = data_query.filter(Price.category == category)
        if city:
            data_query = data_query.filter(Price.city == city)

        data = data_query.group_by(Price.date).all()

        # 🔥 FINAL RETURN
        return {
            "average": float(avg) if avg else 0,
            "daily": [
                {"date": d[0], "average": float(d[1])}
                for d in data
            ]
        }

    finally:
        db.close()