from sqlalchemy import select
from sqlalchemy.orm import Session
from models.tasks import Task
from schemas.tasks import TaskCreate, TaskUpdate


def get_tasks(db: Session, is_completed: bool | None = None) -> list[Task]:
    """タスク一覧を取得する

    args:
    is_completed: 完了か未完了かのステータス

    return:
    タスク一覧を返す。
    (引数に is_completedが渡されている場合は、is_completedに一致するものだけを返す。)
    """
    query = select(Task)

    if is_completed is not None:
        query = query.where(Task.is_completed == is_completed)

    result = db.execute(query)
    return result.scalars().all()


def get_task_by_id(db: Session, task_id: int) -> Task | None:
    """IDを指定して特定のタスクを取得する"""
    return db.get(Task, task_id)


def create_task(db: Session, task_in: TaskCreate) -> Task:
    """新しいタスクを作成する"""
    db_task = Task(**task_in.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, db_task: Task, task_in: TaskUpdate) -> Task:
    """既存のタスクを更新する"""
    update_data = task_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, db_task: Task) -> None:
    """タスクを削除する"""
    db.delete(db_task)
    db.commit()
