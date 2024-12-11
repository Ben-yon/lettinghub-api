from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.db import get_db
from models.user import User
from schemas import UserSchema
from core.utils import verify_password, create_access_token, get_current_user_id
from datetime import timedelta

router = APIRouter()


@router.post("/login")
async def login_for_access_token(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.username).first()
    print(user)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    userObj = {"id": user.id, "email": user.email}
    access_token = create_access_token(data=userObj, expiry=timedelta(days=2))
    refresh_token = create_access_token(data=userObj, refresh=True, expiry=timedelta(days=2))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer",
            "user": UserSchema.UserSchema.from_orm(user)}


@router.get("/users/me/")
async def read_users_me(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema.UserSchema.from_orm(user)