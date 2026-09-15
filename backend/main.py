from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date, timedelta
import os
import httpx
import json

from database import engine, get_db, Base
from models import Todo, Note, Schedule, QuickLink
from schemas import (
    TodoCreate, TodoUpdate, TodoResponse,
    NoteCreate, NoteUpdate, NoteResponse,
    ScheduleCreate, ScheduleUpdate, ScheduleResponse,
    QuickLinkCreate, QuickLinkUpdate, QuickLinkResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PM Workbench API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "PM Workbench API is running", "docs": "/docs"}

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ──── Todos ──────────────────────────────────────────────

@app.get("/api/todos", response_model=List[TodoResponse])
def list_todos(
    completed: Optional[bool] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Todo)
    if completed is not None:
        q = q.filter(Todo.completed == completed)
    if category:
        q = q.filter(Todo.category == category)
    return q.order_by(Todo.priority.desc(), Todo.created_at.desc()).all()


@app.post("/api/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"detail": "Deleted"}


# ──── Notes ──────────────────────────────────────────────

@app.get("/api/notes", response_model=List[NoteResponse])
def list_notes(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Note)
    if category:
        q = q.filter(Note.category == category)
    if search:
        q = q.filter(Note.title.contains(search) | Note.content.contains(search))
    return q.order_by(Note.pinned.desc(), Note.updated_at.desc()).all()


@app.post("/api/notes", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.put("/api/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    for key, value in note.model_dump(exclude_unset=True).items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"detail": "Deleted"}


# ──── Schedules ──────────────────────────────────────────

@app.get("/api/schedules", response_model=List[ScheduleResponse])
def list_schedules(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Schedule)
    if start:
        q = q.filter(Schedule.end_time >= start)
    if end:
        q = q.filter(Schedule.start_time <= end)
    return q.order_by(Schedule.start_time.asc()).all()


@app.post("/api/schedules", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = Schedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


@app.put("/api/schedules/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(schedule_id: int, schedule: ScheduleUpdate, db: Session = Depends(get_db)):
    db_schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    for key, value in schedule.model_dump(exclude_unset=True).items():
        setattr(db_schedule, key, value)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


@app.delete("/api/schedules/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(db_schedule)
    db.commit()
    return {"detail": "Deleted"}


# ──── Quick Links ────────────────────────────────────────

@app.get("/api/quicklinks", response_model=List[QuickLinkResponse])
def list_quick_links(db: Session = Depends(get_db)):
    return db.query(QuickLink).order_by(QuickLink.sort_order.asc()).all()


@app.post("/api/quicklinks", response_model=QuickLinkResponse)
def create_quick_link(link: QuickLinkCreate, db: Session = Depends(get_db)):
    db_link = QuickLink(**link.model_dump())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


@app.put("/api/quicklinks/{link_id}", response_model=QuickLinkResponse)
def update_quick_link(link_id: int, link: QuickLinkUpdate, db: Session = Depends(get_db)):
    db_link = db.query(QuickLink).filter(QuickLink.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Quick link not found")
    for key, value in link.model_dump(exclude_unset=True).items():
        setattr(db_link, key, value)
    db.commit()
    db.refresh(db_link)
    return db_link


@app.delete("/api/quicklinks/{link_id}")
def delete_quick_link(link_id: int, db: Session = Depends(get_db)):
    db_link = db.query(QuickLink).filter(QuickLink.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Quick link not found")
    db.delete(db_link)
    db.commit()
    return {"detail": "Deleted"}


# ──── File Upload ────────────────────────────────────────

@app.get("/api/files")
def list_files(path: str = ""):
    base = os.path.join(UPLOAD_DIR, path)
    if not os.path.exists(base):
        return []
    items = []
    for name in sorted(os.listdir(base)):
        full = os.path.join(base, name)
        items.append({
            "name": name,
            "is_dir": os.path.isdir(full),
            "size": os.path.getsize(full) if os.path.isfile(full) else 0,
            "modified": datetime.fromtimestamp(os.path.getmtime(full)).isoformat(),
        })
    return items


@app.post("/api/files/upload")
async def upload_file(file: UploadFile = File(...), path: str = ""):
    dest_dir = os.path.join(UPLOAD_DIR, path)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, file.filename)
    content = await file.read()
    with open(dest, "wb") as f:
        f.write(content)
    return {"filename": file.filename, "size": len(content)}


@app.delete("/api/files")
def delete_file(path: str):
    target = os.path.join(UPLOAD_DIR, path)
    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="File not found")
    if os.path.isfile(target):
        os.remove(target)
    else:
        import shutil
        shutil.rmtree(target)
    return {"detail": "Deleted"}


# ──── Weather & News (proxy) ────────────────────────────

@app.get("/api/weather")
async def get_weather(city: str = "Beijing"):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"https://wttr.in/{city}?format=j1",
                timeout=5.0,
            )
            data = resp.json()
            current = data.get("current_condition", [{}])[0]
            return {
                "city": city,
                "temp_c": current.get("temp_C", ""),
                "feels_like": current.get("FeelsLikeC", ""),
                "humidity": current.get("humidity", ""),
                "weather_desc": current.get("weatherDesc", [{}])[0].get("value", ""),
                "wind_speed": current.get("windspeedKmph", ""),
                "wind_dir": current.get("winddir16Point", ""),
            }
        except Exception:
            return {"city": city, "temp_c": "--", "weather_desc": "Unable to fetch"}


@app.get("/api/news")
async def get_news(count: int = 6):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                "https://newsapi.org/v2/top-headlines",
                params={"country": "cn", "pageSize": count, "apiKey": "demo"},
                timeout=5.0,
            )
            data = resp.json()
            if data.get("status") == "ok":
                return [
                    {"title": a["title"], "url": a["url"], "source": a["source"]["name"]}
                    for a in data.get("articles", []) if a.get("title")
                ]
        except Exception:
            pass
    return []


# ──── Dashboard Stats ────────────────────────────────────

@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db)):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    pending_todos = db.query(Todo).filter(Todo.completed == False).count()
    completed_todos = db.query(Todo).filter(Todo.completed == True).count()
    total_todos = pending_todos + completed_todos

    upcoming_events = db.query(Schedule).filter(
        Schedule.start_time >= datetime.now(),
        Schedule.start_time <= datetime.combine(week_end, datetime.max.time()),
    ).count()

    overdue_todos = db.query(Todo).filter(
        Todo.completed == False,
        Todo.due_date < today,
    ).count()

    return {
        "pending_todos": pending_todos,
        "completed_todos": completed_todos,
        "total_todos": total_todos,
        "completion_rate": round(completed_todos / total_todos * 100, 1) if total_todos > 0 else 0,
        "upcoming_events": upcoming_events,
        "overdue_todos": overdue_todos,
        "total_notes": db.query(Note).count(),
    }
