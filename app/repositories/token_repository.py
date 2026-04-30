from app.models.token_model import RefreshTokenModel
from sqlalchemy.orm import Session
from datetime import datetime


def add_refresh_token(db: Session, user_id: int, token: str, exp: datetime):
    token = RefreshTokenModel(
        user_id=user_id, token=token, exp=exp)
    db.add(token)
    db.commit()


def get_token(db: Session, token: str) -> RefreshTokenModel | None :
    token_obj = db.query(RefreshTokenModel).filter_by(token=token).one_or_none()
    return token_obj


def delete_token(db: Session, token: str):
    token_obj = db.query(RefreshTokenModel).filter_by(token=token).one_or_none()
    try:
        db.delete(token_obj)
        db.commit()
    except Exception:
        raise Exception
