from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate
from app.auth import hash_password,verify_password, create_token
from app.deps import get_db

router = APIRouter()

# REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    # check existing user
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    #ROLE LOGIC (IMPORTANT)
    role = "admin" if user.username.lower().startswith("admin") else "viewer"

    new_user = User(
        username=user.username,
        password=hash_password(user.password),  # 🔐 HASH
        role=role
    )

    db.add(new_user)
    db.commit()

    return {"message": f"{role} user created"}


# LOGIN
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "username": db_user.username,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "role": db_user.role
    }