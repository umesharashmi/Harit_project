from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import router as main_router
from app.auth_routes import router as auth_router

from services.processor import process_all
from services.tourism_processor import process_country

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(main_router)
app.include_router(auth_router)

# STARTUP
@app.on_event("startup")
def startup_event():
    print("🚀 STARTING...")

    try:
        # 1. price processing
        process_all()
        process_country()

    

        
        print("✅ DONE")

    except Exception as e:
        print("❌ ERROR:", e)