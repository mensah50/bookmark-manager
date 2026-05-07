from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field


class BookmarkBase(BaseModel):
    url: HttpUrl
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class BookmarkCreate(BookmarkBase):
    tags: List[str] = Field(default_factory=list)


class BookmarkUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    tags: Optional[List[str]] = None


class BookmarkRead(BookmarkBase):
    id: int
    created_at: datetime
    tags: List[str]

    class Config:
        from_attributes = True
