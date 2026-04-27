from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated
from .task_schemas import TaskResponseSchema


class UserBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: Annotated[
        str, Field(max_length=30,
                   description="the username of the user, it is unique")]
    email: Annotated[
        EmailStr, Field(max_length=30,
                        description="the email of the user")]


class UserRegisterSchema(UserBaseSchema):
    password: Annotated[
        str, Field(min_length=8, max_length=16,
                   description="the password of the user")]


class UserResponseSchema(UserBaseSchema):
    id: int


class UserLogInSchema(BaseModel):
    username: Annotated[
        str, Field(max_length=30,
                   description="the username of the user, it is unique")]
    password: Annotated[
        str, Field(min_length=8, max_length=16,
                   description="the password of the user")]
