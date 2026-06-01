from pydantic import BaseModel, ConfigDict, Field, EmailStr

from typing import Optional
from datetime import datetime, UTC

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(max_length=120)
    hash_password: str = Field(min_length=4)
    create_at: datetime = Field(default=datetime.now(UTC))


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    hash_password: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: EmailStr
    create_at: datetime


class WorkoutCreate(BaseModel):
    exercise_name: str = Field(min_length=3)
    wights: int = Field(ge=0, default=0)
    sets: int = Field(ge=1)
    reps: int = Field(ge=1)
    rest_time: int = Field(default=0)
    image: str = Field(default="None")


class WorkoutUpdate(BaseModel):
    exercise_name: str | None = None
    wights: int | None = None
    sets: int | None = None
    reps: int | None = None
    rest_time: int | None = None
    image: str | None = None


class WorkoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    exercise_name: str 
    wights: int 
    sets: int 
    reps: int 
    rest_time: int 
    image: Optional[str] = None

    user_id:  str
