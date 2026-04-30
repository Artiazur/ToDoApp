from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.core import security
from app.schemas.user_schemas import UserRegisterSchema


def make_aware_datetime_object(expires_at: datetime) -> datetime:
    if not expires_at.tzinfo:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
        return expires_at
    return expires_at


def is_token_type_valid(payload: dict) -> bool:
    if payload.get("type") != "refresh":
        return False
    return True
            
            
def is_user_id_valid(payload_id: int, db_id: int) -> bool:
    if payload_id != db_id:
        return False
    return True


def check_refresh_token(token: str, id: int):
    try:
        payload = security.decode_token(token)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"}
        )
 
    if not is_token_type_valid(payload):
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    user_id = payload.get("user_id")
    if not is_user_id_valid(user_id, id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user_id


