from src.repositories import tasks as task_repository
from src.schemas.tasks import TaskCreate, TaskUpdate


def test_create_task(db_session):
    """タスクがDBに保存されること"""
    task_in = TaskCreate(title="DBテストタスク", description="詳細")
    task = task_repository.create_task(db_session, task_in=task_in)

    assert task.id is not None
    assert task.title == "DBテストタスク"
    assert task.is_completed is False


def test_get_task_by_id(db_session):
    """IDでタスクを取得できること"""
    task_in = TaskCreate(title="取得テスト")
    created_task = task_repository.create_task(db_session, task_in=task_in)

    fetched_task = task_repository.get_task_by_id(db_session, task_id=created_task.id)
    assert fetched_task is not None
    assert fetched_task.id == created_task.id


def test_get_tasks_filter(db_session):
    """完了状態でタスクをフィルタリング取得できること"""
    # テストデータの準備
    task1 = task_repository.create_task(db_session, TaskCreate(title="未完了"))
    task2 = task_repository.create_task(db_session, TaskCreate(title="完了予定"))
    task_repository.update_task(
        db_session, db_task=task2, task_in=TaskUpdate(is_completed=True)
    )

    # 未完了のみ取得
    uncompleted = task_repository.get_tasks(db_session, is_completed=False)
    assert len(uncompleted) == 1
    assert uncompleted[0].id == task1.id

    # 完了のみ取得
    completed = task_repository.get_tasks(db_session, is_completed=True)
    assert len(completed) == 1
    assert completed[0].id == task2.id


def test_delete_task(db_session):
    """タスクが削除されること"""
    task_in = TaskCreate(title="削除テスト")
    task = task_repository.create_task(db_session, task_in=task_in)

    task_repository.delete_task(db_session, db_task=task)
    fetched_task = task_repository.get_task_by_id(db_session, task_id=task.id)
    assert fetched_task is None
