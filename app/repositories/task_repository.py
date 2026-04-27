from fastapi import Depends, Path
from app.core.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated, Any
from app.models.task_model import TaskModel
from app.schemas import task_schemas


def get_all(db: Session, user_id: int):
    try:
        all_tasks = db.query(TaskModel).filter_by(user_id=user_id).all()
        return all_tasks
    except:
        return None


def get_one_task(
    db: Session,
    task_id: int,
    user_id: int
) -> TaskModel:
    task = db.query(TaskModel).filter_by(
        user_id=user_id, id=task_id).one_or_none()
    return task


def create_task(
    db: Session,
    task_schema: task_schemas.TaskCreateSchema,
    user_id: int
) -> TaskModel:
    task_dict = task_schema.model_dump()
    task_dict.update({"user_id": user_id})
    task = TaskModel(**task_dict)
    db.add(task)
    db.commit()
    return task


def update_task(
    db: Session,
    task_schema: task_schemas.TaskUpdateSchema,
    task_id: int,
    user_id: int
) -> TaskModel:
    task = db.query(TaskModel).filter_by(
        user_id=user_id, id=task_id).one_or_none()
    if task:
        task_dict = task_schema.model_dump(exclude_unset=True)
        for fields, values in task_dict.items():
            setattr(task, fields, values)  # task.field = value
        db.commit()
        db.refresh(task)
        return task
    return task


def delete_task(
    db: Session,
    task_id: int,
    user_id: int
):
    task = db.query(TaskModel).filter_by(
        user_id=user_id, id=task_id).one_or_none()
    try:
        db.delete(task)
        db.commit()
        return True
    except:
        return False
