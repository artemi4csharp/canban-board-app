
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.dependencies import get_db
from app.auth.auth import hash_password, verify_password, create_access_token, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(email=user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(email=form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token({'sub': str(db_user.id)})
    return {'access_token': token, 'token_type': 'bearer'}

@router.get("/protected")
def read_protected(token: str = Depends(oauth2_scheme)):
    return {"token": token}

