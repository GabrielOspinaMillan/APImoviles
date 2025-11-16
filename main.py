from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import crud
import schemas
from utils import check_idempotency

Base.metadata.create_all(bind=engine)

app = FastAPI(title="To-Do API Offline-First")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks", response_model=list[schemas.TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


@app.post("/tasks", response_model=schemas.TaskResponse)
def create_task(
    data: schemas.TaskCreate,
    db: Session = Depends(get_db),
    idem=Depends(check_idempotency)
):
    if crud.get_task(db, data.id):
        raise HTTPException(400, "Task already exists with this ID")
    return crud.create_task(db, data)


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: str,
    data: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    task = crud.update_task(db, task_id, data)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = crud.delete_task(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return {"status": "deleted"}

