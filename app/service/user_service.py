from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core import security
from app.schemas import user_schemas
from app.repositories import user_repository, token_repository
from app.models.user_model import UserModel
from datetime import datetime, timezone


def user_login(
    db: Session,
    username: str,
    password: str
):
    user_obj = user_repository.get_user_by_username(db, username)

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    is_valid = security.verify_password(password, user_obj.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    refresh_token, exp = security.create_refresh_token(
        {"user_id": user_obj.id})
    token_repository.add_refresh_token(db, user_obj.id, refresh_token, exp)
    access_token = security.create_access_token({"user_id": user_obj.id})
    return {"access_token": access_token,
            "refresh_token": refresh_token}


def register_user(
    db: Session,
    user: user_schemas.UserRegisterSchema
):
    user_obj = user_repository.get_user_by_username(db, user.username.lower())
    if user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username exist"
        )
        
    """
    یه 
    helper_service 
    بساز که یه تابع داشته باشه
    بعد توی اون تابع یه شِمای جدید بسازه برای کاربر و آبجکتش رو برگردونه.
    """
    hashed_pass = security.hash_password(user.password)
    user.password = hashed_pass
    username = user.username
    user.username = username.lower()
    registered_user = user_repository.create_user(db, user)
    return registered_user


def get_current_active_user(
    db: Session,
    user_id: int
) -> UserModel:
    user_obj = user_repository.get_user_by_id(db, user_id)
    if not user_obj:
        raise HTTPException(
            status_code=401,
            detail="""INVALID CREDENTIALS"""
        )
    return user_obj


def refresh_access_token(db: Session, token: str):
    token_obj = token_repository.get_token(db, token)

    if not token_obj:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    """اینجا هم بهتره که تو همون ماژول کمک کننده این کارو بکنم"""
    
    expires_at = token_obj.exp
    if not expires_at.tzinfo:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = security.create_access_token({"user_id": token_obj.user_id})
    
    #باید رفرش توکن جدید بسازم و قبلی رو پاک کنم

    return {"access_token": access_token}
