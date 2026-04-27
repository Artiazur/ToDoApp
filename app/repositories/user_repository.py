from app.models.user_model import UserModel
from app.models.task_model import TaskModel
from app.core import security
from app.schemas import user_schemas
from sqlalchemy.orm import Session


def get_user_by_username(db: Session, username: str) -> UserModel | None:
    user = db.query(UserModel).filter_by(username=username).one_or_none()
    return user


def get_user_by_id(db: Session, user_id: int) -> UserModel | None:
    user = db.query(UserModel).filter_by(id=user_id).one_or_none()
    return user


def create_user(db: Session, user: user_schemas.UserRegisterSchema):
    user_obj = UserModel(**user.model_dump())
    db.add(user_obj)
    db.commit()
    return user_obj



