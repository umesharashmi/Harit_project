from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import router as main_router
from app.auth_routes import router as auth_router

from services.processor import process_all
from services.tourism_processor import process_country

from scheduler import start_scheduler

app = FastAPI(title="Harit API")

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "Harit API is running 🚀"}

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://harit-project-fj4v.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DATABASE ----------------
Base.metadata.create_all(bind=engine)

# ---------------- ROUTES ----------------
app.include_router(main_router)
app.include_router(auth_router)

# ---------------- STARTUP ----------------
@app.on_event("startup")
def startup_event():
    print("🚀 HARIT API STARTING...")
    start_scheduler()

    try:
        process_all()
        process_country()
        print("✅ STARTUP TASKS DONE")

    except Exception as e:
        print("❌ STARTUP ERROR:", e)