from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app.database import Base, engine
from app.routes import router as main_router
from app.auth_routes import router as auth_router

#from services.processor import process_all
#from services.tourism_processor import process_country
from services.cse_processor import process_cse

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
STARTED = False  # 🔥 guard flag

@app.on_event("startup")
async def startup_event():
    global STARTED

    print("🚀 HARIT API STARTING...")

    # 🔥 prevent duplicate execution
    if STARTED:
        print("⚠️ Startup already executed. Skipping...")
        return

    STARTED = True

    # Start scheduler
    start_scheduler()

    # Run heavy tasks in background thread
    async def run_tasks():
        try:
            print("⏳ Processing data...")

            #process_all()
            #process_country()
            await asyncio.to_thread(process_cse)  # 🔥 FIX (no crash)

            print("✅ STARTUP TASKS DONE")

        except Exception as e:
            print("❌ STARTUP ERROR:", e)

    asyncio.create_task(run_tasks())