from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.repositories import task_repository
from app.models.task_model import TaskModel
from app.schemas import task_schemas
from sqlalchemy.orm import Session


def get_all(db: Session, user_id: int) -> list[TaskModel]:
    all_tasks = task_repository.get_all(db, user_id)
    if not all_tasks:
        raise HTTPException(
            status_code=404, detail="YOU HAVEN'T MADE ANY TASKS YET!")
    else:
        return all_tasks


def get_one_task(
    db: Session,
    task_id: int,
    user_id: int
) -> TaskModel:
    task = task_repository.get_one_task(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="TASK NOT FOUND!")
    else:
        return task


def create_new_task(
    db: Session,
    task_schema: task_schemas.TaskCreateSchema,
    user_id: int
) -> TaskModel:
    new_task = task_repository.create_task(db, task_schema, user_id)
    if not new_task:
        raise HTTPException(status_code=404, detail="TASK IS NOT CREATED!")
    return new_task


def update_task(
    db: Session,
    task_schema: task_schemas.TaskUpdateSchema,
    task_id: int,
    user_id: int
) -> TaskModel:
    updated_task = task_repository.update_task(
        db, task_schema, task_id, user_id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="TASK IS NOT FOUND!")
    return updated_task


def delete_task(
    db: Session,
    task_id: int,
    user_id: int
):
    is_deleted = task_repository.delete_task(db, task_id, user_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Task is not found")
    return JSONResponse(content="Task deleted successfully", status_code=200)
