from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.column import BoardColumn
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut
from app.dependencies import get_db
from app.auth.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    column = (
        db.query(BoardColumn)
        .filter(BoardColumn.id == task.column_id, BoardColumn.user_id == user.id)
        .first()
    )
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")

    max_position = (
        db.query(func.max(Task.position))
        .filter(Task.column_id == column.id)
        .scalar()
    )
    next_position = (max_position or 0) + 1

    new_task = Task(
        title=task.title,
        description=task.description,
        column_id=task.column_id,
        user_id=user.id,
        position=next_position
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_task = db.query(Task).filter_by(id=task_id, user_id=user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_task = db.query(Task).filter_by(id=task_id, user_id=user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.description = task.description
    db_task.column_id = task.column_id
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_task = db.query(Task).filter_by(id=task_id, user_id=user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted successfully"}

@router.put('/{task_id}/move')
def move_task(task_id: int, new_position: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.query(Task).join(BoardColumn).filter(Task.id==task_id, BoardColumn.user_id==user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks = (
        db.query(Task)
        .filter(Task.column_id==task.column_id)
        .order_by(Task.position)
        .all()
    )

    tasks.remove(task)

    tasks.insert(new_position - 1, task)
    db.commit()
    return {"detail": "Task moved successfully"}


