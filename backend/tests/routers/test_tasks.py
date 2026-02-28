from fastapi import status


def test_read_tasks_empty(client):
    """初期状態で空のリストが返ること"""
    response = client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_task_route(client):
    """POST /tasks の正常系"""
    response = client.post("/tasks", json={"title": "ルーターテスト"})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "ルーターテスト"
    assert "id" in data


def test_read_task_not_found(client):
    """存在しないタスクIDを指定した場合に404が返ること"""
    response = client.get("/tasks/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"


def test_update_task_route(client):
    """PATCH /tasks/{id} の正常系"""
    # 事前作成
    create_res = client.post("/tasks", json={"title": "変更前"})
    task_id = create_res.json()["id"]

    # 更新リクエスト
    response = client.patch(
        f"/tasks/{task_id}", json={"title": "変更後", "is_completed": True}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "変更後"
    assert response.json()["is_completed"] is True


def test_delete_task_route(client):
    """DELETE /tasks/{id} の正常系と異常系"""
    # 事前作成
    create_res = client.post("/tasks", json={"title": "削除ターゲット"})
    task_id = create_res.json()["id"]

    # 削除リクエスト
    delete_res = client.delete(f"/tasks/{task_id}")
    assert delete_res.status_code == status.HTTP_204_NO_CONTENT

    # 削除済みのIDを再度削除しようとすると404
    delete_res_again = client.delete(f"/tasks/{task_id}")
    assert delete_res_again.status_code == status.HTTP_404_NOT_FOUND
