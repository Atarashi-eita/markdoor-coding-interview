from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
from repositories import tasks as task_repository

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def read_tasks(is_completed: bool | None = None, db: Session = Depends(get_db)):
    """タスク一覧を取得する（クエリパラメータでフィルタリング可能）"""
    return task_repository.get_tasks(db, is_completed=is_completed)


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """指定されたIDのタスクを取得する"""
    db_task = task_repository.get_task_by_id(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return db_task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    """新しいタスクを作成する"""
    return task_repository.create_task(db, task_in=task_in)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db)):
    """指定されたIDのタスクを更新する（部分更新）"""
    db_task = task_repository.get_task_by_id(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task_repository.update_task(db, db_task=db_task, task_in=task_in)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """指定されたIDのタスクを削除する"""
    db_task = task_repository.get_task_by_id(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    task_repository.delete_task(db, db_task=db_task)
    return None
