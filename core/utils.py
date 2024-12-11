import jwt
import bcrypt
from core.config import settings
from fastapi import Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import time
import logging
from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


# Hash a password using bcrypt
def get_password_hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')


# Check if the provided password matches the stored password (hashed)
def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')

    # If the hashed_password is stored as a string, convert it back to bytes
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')

    # Ensure the salt is valid before checking the password
    try:
        return bcrypt.checkpw(password_byte_enc, hashed_password)
    except ValueError as e:
        if "Invalid salt" in str(e):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid salt",
            )
        else:
            raise e


def create_access_token(data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}
    payload["user"] = data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decode JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Optionally, you can check roles, permissions, or user status here
        return payload.get('user')
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def get_current_user_id(user: dict = Depends(verify_token)):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="unauthorized user")
    # Access the user ID using dictionary key-based access
    user_id = user['id']

    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data")

    return user_id


def get_organization(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    return user.organization