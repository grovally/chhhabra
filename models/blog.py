from pydantic import BaseModel
from typing import Optional


class BlogCreate(BaseModel):
    title: str
    description: str
    content: str
    category: str
    author: str
    image: str
    published: bool = True


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    image: Optional[str] = None
    published: Optional[bool] = None