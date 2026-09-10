import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.database import User, get_db
router=APIRouter(prefix="/api/auth", tags=["authentication"])
pwd=CryptContext(schemes=["bcrypt"], deprecated="auto")
class Credentials(BaseModel): email: EmailStr; password: str = Field(min_length=8, max_length=128)
def public(u): return {"id":u.id,"email":u.email}
def token_for(user):
    payload={"sub":str(user.id),"email":user.email,"exp":datetime.now(timezone.utc)+timedelta(hours=8)}
    return jwt.encode(payload,os.getenv("SECRET_KEY","development-only-change-me"),algorithm="HS256")
@router.post("/signup", status_code=201)
def signup(data: Credentials, db: Session=Depends(get_db)):
    if db.query(User).filter_by(email=data.email.lower()).first(): raise HTTPException(409,"Email already registered")
    user=User(email=data.email.lower(), password_hash=pwd.hash(data.password)); db.add(user); db.commit(); db.refresh(user)
    return {**public(user),"access_token":token_for(user),"token_type":"bearer"}
@router.post("/login")
def login(data: Credentials, db: Session=Depends(get_db)):
    user=db.query(User).filter_by(email=data.email.lower()).first()
    if not user or not pwd.verify(data.password,user.password_hash): raise HTTPException(401,"Invalid email or password")
    return {**public(user),"access_token":token_for(user),"token_type":"bearer"}
