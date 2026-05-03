from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import router as main_router
from app.auth_routes import router as auth_router

app = FastAPI(title="Harit API")

# ---------------- ROOT ROUTE ----------------
@app.get("/")
def root():
    return {"message": "Harit API is running 🚀"}

# ---------------- CORS (FIXED) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
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
    print("✅ API READY")