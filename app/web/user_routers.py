from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.service import user_service
from app.schemas import user_schemas
from app.core import database
from .dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login")
def log_in(
    db: Annotated[Session, Depends(database.get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return user_service.user_login(db, form_data.username, form_data.password)


@router.post(
    "/register",
    response_model=user_schemas.UserResponseSchema,
    status_code=201
)
def sign_up(
    db: Annotated[Session, Depends(database.get_db)],
    user: user_schemas.UserRegisterSchema,
):
    return user_service.register_user(db, user)


@router.get("/me", response_model=user_schemas.UserResponseSchema)
def get_me(
    db: Annotated[Session, Depends(database.get_db)],
    user_id: Annotated[int, Depends(get_current_user)],
):
    return user_service.get_current_user_profile(db, user_id)


@router.post("/refresh")
def refresh(db: Annotated[Session, Depends(database.get_db)], refresh_token: str):
    return user_service.refresh_access_token(db, refresh_token)
