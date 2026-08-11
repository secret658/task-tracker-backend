def test_create_task_requires_auth(client):
#проверяем что нельзя создать задачу без токена авторизации
    response = client.post("/tasks/", json={"title": "Test task"})
    #отправляем запрос БЕЗ заголовка Authorization

    assert response.status_code in (401, 403)
    #FastAPI/HTTPBearer может вернуть 401 или 403 в зависимости от деталей реализации,
    #проверяем оба варианта через кортеж


def test_create_task_with_auth(client):
#проверяем что создание задачи работает при наличии токена
    client.post(
        "/auth/register",
        json={"email": "tasktest@example.com", "password": "password123"},
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "tasktest@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]
    #достаем токен из ответа логина

    response = client.post(
        "/tasks/",
        json={"title": "Test task"},
        headers={"Authorization": f"Bearer {token}"},
        #прикладываем токен в заголовке, точно так же как это делает реальный клиент
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert data["is_done"] is False

def test_streak_zero_for_new_user(client):
#проверяем что у нового юзера без истории стрик равен 0
    client.post(
        "/auth/register",
        json={"email": "streaktest@example.com", "password": "password123"},
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "streaktest@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/tasks/streak",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["streak"] == 0