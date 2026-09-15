from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class TodoCreate(BaseModel):
    title: str
    description: str = ""
    completed: bool = False
    priority: int = 0
    due_date: Optional[date] = None
    category: str = "general"


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = None
    due_date: Optional[date] = None
    category: Optional[str] = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    priority: int
    due_date: Optional[date]
    category: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoteCreate(BaseModel):
    title: str
    content: str = ""
    category: str = "general"
    pinned: bool = False


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    pinned: Optional[bool] = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    pinned: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScheduleCreate(BaseModel):
    title: str
    description: str = ""
    start_time: datetime
    end_time: datetime
    all_day: bool = False
    color: str = "#4F46E5"
    location: str = ""


class ScheduleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    all_day: Optional[bool] = None
    color: Optional[str] = None
    location: Optional[str] = None


class ScheduleResponse(BaseModel):
    id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    all_day: bool
    color: str
    location: str
    created_at: datetime

    class Config:
        from_attributes = True


class QuickLinkCreate(BaseModel):
    title: str
    url: str
    icon: str = "🔗"
    category: str = "general"
    sort_order: int = 0


class QuickLinkUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    icon: Optional[str] = None
    category: Optional[str] = None
    sort_order: Optional[int] = None


class QuickLinkResponse(BaseModel):
    id: int
    title: str
    url: str
    icon: str
    category: str
    sort_order: int
    created_at: datetime

    class Config:
        from_attributes = True
