from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate
from datetime import datetime

def get_tasks(db: Session):
    return db.query(Task).all()

def get_task(db: Session, task_id: str):
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, data: TaskCreate):
    task = Task(
        id=data.id,
        title=data.title,
        completed=data.completed,
        updated_at=data.updatedAt
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task_id: str, data: TaskUpdate):
    task = get_task(db, task_id)
    if task:
        task.title = data.title
        task.completed = data.completed
        task.updated_at = data.updatedAt
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: str):
    task = get_task(db, task_id)
    if task:
        db.delete(task)
        db.commit()
    return task