from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.auth.models import User
from src.auth.schemas import SignupSchema, LoginSchema
from src.auth.utils import hashpw, checkpw

router = APIRouter(
    prefix="/api/auth"
)

@router.post("/signup")
def auth_signup(user: SignupSchema, db: Session=Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = hashpw(user.password)
    db_user = User(
        email=user.email, password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"response": "signup success!"}

@router.post("/login")
def auth_login(user: LoginSchema, db: Session=Depends(get_db)):
    return {"response": "login"}
