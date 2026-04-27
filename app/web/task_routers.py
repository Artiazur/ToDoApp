from fastapi import APIRouter, Path, Body, Depends, HTTPException
from typing import Annotated
from app.service import task_service
from app.schemas import task_schemas
from app.core.database import get_db
from sqlalchemy.orm import Session
from .dependencies import get_current_user


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/all_tasks", response_model=list[task_schemas.TaskResponseSchema])
def retrieve_all_tasks(
        db: Annotated[Session, Depends(get_db)],
        user_id: Annotated[int, Depends(get_current_user)]):
    return task_service.get_all(db, user_id)


@router.get("/{task_id}", response_model=task_schemas.TaskResponseSchema)
def retrieve_one_task(
    db: Annotated[Session, Depends(get_db)],
    task_id: Annotated[int, Path(gt=0)],
    user_id: Annotated[int, Depends(get_current_user)]
):
    return task_service.get_one_task(db, task_id, user_id)


@router.post("/create_task", response_model=task_schemas.TaskResponseSchema)
def create_new_task(
    db: Annotated[Session, Depends(get_db)],
    task_schema: Annotated[task_schemas.TaskCreateSchema, Body()],
    user_id: Annotated[int, Depends(get_current_user)]
):
    return task_service.create_new_task(db, task_schema, user_id)


@router.put("/update_task/{task_id}", response_model=task_schemas.TaskResponseSchema)
def update_task(
    db: Annotated[Session, Depends(get_db)],
    task_schema: Annotated[task_schemas.TaskUpdateSchema, Body()],
    task_id: Annotated[int, Path(gt=0)],
    user_id: Annotated[int, Depends(get_current_user)]
):
    return task_service.update_task(db, task_schema, task_id, user_id)


@router.delete("/delete_task/{task_id}")
async def delete_task(
    db: Annotated[Session, Depends(get_db)],
    task_id: Annotated[int, Path(gt=0)],
    user_id: Annotated[int, Depends(get_current_user)]
):
    return task_service.delete_task(db, task_id, user_id)
