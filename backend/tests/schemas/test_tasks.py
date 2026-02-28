import pytest
from pydantic import ValidationError
from src.schemas.tasks import TaskCreate, TaskUpdate


def test_task_create_valid():
    """正常なデータでTaskCreateが生成できること"""
    task = TaskCreate(title="タスクのタイトル", description="説明文")
    assert task.title == "タスクのタイトル"
    assert task.description == "説明文"


def test_task_create_title_too_long():
    """タイトルが30文字を超えた場合にValidationErrorになること"""
    with pytest.raises(ValidationError):
        TaskCreate(title="あ" * 31)


def test_task_create_title_empty():
    """タイトルが空(1文字未満)の場合にValidationErrorになること"""
    with pytest.raises(ValidationError):
        TaskCreate(title="")


def test_task_update_valid():
    """TaskUpdateが正常に生成できること（全フィールド任意）"""
    task = TaskUpdate(title="更新タイトル", is_completed=True)
    assert task.title == "更新タイトル"
    assert task.is_completed is True
