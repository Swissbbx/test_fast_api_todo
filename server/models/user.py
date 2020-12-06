from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class TodoSchema(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    due_date: datetime = Field(...)
    is_done: bool = False

class UserInput(BaseModel):
    username: EmailStr = Field(...)
    plain_password: str = Field(...)

class User(BaseModel):
    username: EmailStr = Field(...)
    disabled: Optional[bool] = None
    hashed_password: str = Field(...)
    tasks: Optional[List[TodoSchema]] = []

   
class UserInDB(User):
    hashed_password: str


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}