from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

# 🔐 Bearer security object
security = HTTPBearer()

# 📦 DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 👤 Get current logged user
def get_current_user(credentials = Depends(security), db: Session = Depends(get_db)):

    token = credentials.credentials   # 🔥 Bearer token eka extract karanawa

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def admin_only(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user