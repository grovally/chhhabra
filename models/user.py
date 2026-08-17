from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = "Admin"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str