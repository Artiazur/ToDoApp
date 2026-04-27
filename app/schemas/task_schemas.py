from pydantic import BaseModel, Field
from typing import Annotated


class TaskBaseSchema(BaseModel):
    title: Annotated[
        str, Field(max_length=30,
                   description="the title of the task")]
    description: Annotated[
        str | None, Field(max_length=500,
                          description="the desription of the task, it is optional")
    ] = None
    is_completed: Annotated[
        bool,
        Field(description="the status of the task")
    ] = False


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(TaskBaseSchema):
    id: Annotated[int, Field(description="unique identifier of the task")]
