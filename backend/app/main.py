from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router
from services.processor import process_all
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

#VERY IMPORTANT CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# create tables
Base.metadata.create_all(bind=engine)

# include routes
app.include_router(router)

# RUN ON START (CORRECT WAY)
@app.on_event("startup")
def startup_event():
    process_all()