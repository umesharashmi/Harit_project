from fastapi import APIRouter, HTTPException
from sqlalchemy import func
from .database import SessionLocal
from .models import Price,User,CountryArrival,EquityMovement
from services.parser import parse_pdf
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends
from app.deps import get_current_user, admin_only

router = APIRouter()


@router.get("/prices")
def get_all_prices(
    item: str = None,
    category: str = None,
    city: str = None,
    start: str = None,
    end: str = None,
    user: User = Depends(get_current_user)
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
def filters(user: User = Depends(get_current_user)):
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

        #  backend folder
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        #  pdf folder
        pdf_folder = os.path.join(BASE_DIR, "pdfs")

        #  check folder
        if not os.path.exists(pdf_folder):
            return {"error": f"PDF folder not found: {pdf_folder}"}

        
        # CLEAR OLD DATA FIRST
        
        deleted = db.query(Price).delete()
        db.commit()

        print(f"OLD DATA CLEARED: {deleted} rows")

       
        #  LOAD NEW DATA
        
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


#  SINGLE DATE AVG
@router.get("/avg")
def average(date: str = None, item: str = None, category: str = None, city: str = None,user: User = Depends(get_current_user)):
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


#  RANGE AVG ( FIXED SAFE VERSION)
@router.get("/avg-range")
def avg_range(start: str, end: str, item: str = None, category: str = None, city: str = None,user: User = Depends(get_current_user)):
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


@router.get("/country/filters")
def country_filters():
    db = SessionLocal()
    try:
        countries = [c[0] for c in db.query(CountryArrival.country).distinct()]
        years = [y[0] for y in db.query(CountryArrival.year).distinct()]

        return {
            "countries": countries,
            "years": sorted(years),
            "months": [
                "jan","feb","mar","apr","may","jun",
                "jul","aug","sep","oct","nov","dec"
            ]
        }
    finally:
        db.close()

@router.get("/country/search")
def search_country(year: int = None, country: str = None, month: str = None):
    db = SessionLocal()

    try:
        query = db.query(CountryArrival)

        # FIX: year optional
        if year is not None:
            query = query.filter(CountryArrival.year == year)

        if country:
            query = query.filter(CountryArrival.country == country)

        rows = query.all()

        result = []

        for r in rows:
            if month:
                value = getattr(r, month, 0)
            else:
                value = r.total

            result.append({
                "country": r.country,
                "year": r.year,
                "month": month,
                "count": value
            })

        return result

    finally:
        db.close()


@router.get("/country/total-by-year-calc")
def total_by_year_calc():
    db = SessionLocal()

    try:
        result = db.query(
            CountryArrival.year,
            func.sum(
                CountryArrival.jan +
                CountryArrival.feb +
                CountryArrival.mar +
                CountryArrival.apr +
                CountryArrival.may +
                CountryArrival.jun +
                CountryArrival.jul +
                CountryArrival.aug +
                CountryArrival.sep +
                CountryArrival.oct +
                CountryArrival.nov +
                CountryArrival.dec
            ).label("total_arrivals")
        ).group_by(CountryArrival.year).all()

        return [
            {
                "year": r[0],
                "total_arrivals": int(r[1]) if r[1] else 0
            }
            for r in result
        ]

    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/equity/filters")
def equity_filters(db: Session = Depends(get_db)):

    return {
        "companies": [
            c[0] for c in db.query(EquityMovement.company_name).distinct().all()
        ],
        "industries": [
            i[0] for i in db.query(EquityMovement.industry_group).distinct().all()
        ],
        "boards": [
            b[0] for b in db.query(EquityMovement.board).distinct().all()
        ],
        "dates": [
            d[0] for d in db.query(EquityMovement.report_date).distinct().all()
        ],
    }



@router.get("/equity/chart")
def equity_chart(
    company: str = None,
    industry: str = None,
    board: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(
        EquityMovement.last_traded_date,
        func.avg(EquityMovement.close_price),
        func.sum(EquityMovement.turnover),
        func.sum(EquityMovement.quantity)
    )

    if company:
        query = query.filter(EquityMovement.company_name == company)

    if industry:
        query = query.filter(EquityMovement.industry_group == industry)

    if board:
        query = query.filter(EquityMovement.board == board)

    # ✅ FIXED TYPO HERE
    data = query.group_by(EquityMovement.last_traded_date).all()

    return {
        "labels": [d[0] for d in data],
        "avg_price": [float(d[1] or 0) for d in data],
        "turnover": [float(d[2] or 0) for d in data],
        "quantity": [int(d[3] or 0) for d in data],
    }

from sqlalchemy import and_

@router.get("/equity/change-over-period")
def equity_change_over_period(
    company: str = None,
    industry: str = None,
    board: str = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(
        EquityMovement.report_date,
        func.avg(EquityMovement.close_price).label("avg_price"),
        func.sum(EquityMovement.turnover).label("turnover"),
        func.sum(EquityMovement.quantity).label("quantity")
    )

    if company:
        query = query.filter(EquityMovement.company_name == company)

    if industry:
        query = query.filter(EquityMovement.industry_group == industry)

    if board:
        query = query.filter(EquityMovement.board == board)

    if start_date and end_date:
        query = query.filter(
            and_(
                EquityMovement.report_date >= start_date,
                EquityMovement.report_date <= end_date
            )
        )

    # ✅ FIXED HERE (was wrong column before)
    data = query.group_by(EquityMovement.report_date)\
                .order_by(EquityMovement.report_date)\
                .all()

    return {
        "labels": [d[0] for d in data],
        "avg_price": [float(d[1] or 0) for d in data],
        "turnover": [float(d[2] or 0) for d in data],
        "quantity": [int(d[3] or 0) for d in data],
    }

@router.get("/equity/filters")
def equity_filters(db: Session = Depends(get_db)):

    dates = db.query(EquityMovement.last_traded_date).distinct().all()

    clean_dates = sorted([d[0] for d in dates])

    return {
        "companies": [c[0] for c in db.query(EquityMovement.company_name).distinct().all()],
        "industries": [i[0] for i in db.query(EquityMovement.industry_group).distinct().all()],
        "boards": [b[0] for b in db.query(EquityMovement.board).distinct().all()],
        "dates": clean_dates
    }