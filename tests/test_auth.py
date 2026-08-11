def test_register_new_user(client):
#client - это та самая fixture из conftest.py, pytest сам подставит её сюда
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    #отправляем тестовый POST запрос, точно так же как делали руками в Swagger

    assert response.status_code == 200
    #assert - проверка, если условие False, тест падает с ошибкой
    #проверяем что сервер ответил успехом

    data = response.json()
    #превращаем ответ сервера из JSON в питоновский словарь
    assert data["email"] == "test@example.com"
    #проверяем что email в ответе совпадает с тем, что отправляли
    assert "hashed_password" not in data
    #важная проверка безопасности - хэш пароля не должен утекать в ответ API


def test_register_duplicate_email(client):
#проверяем что нельзя зарегистрироваться дважды с одним email
    client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "testpassword123"},
    )
    #первая регистрация должна пройти успешно

    response = client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "anotherpassword"},
    )
    #вторая попытка с тем же email

    assert response.status_code == 400
    #ожидаем именно ошибку 400, которую мы сами настраивали в user_service.py

def test_login_correct_password(client):
#проверяем что логин с правильным паролем дает токен
    client.post(
        "/auth/register",
        json={"email": "login_test@example.com", "password": "correctpassword"},
    )
    #сначала регистрируем юзера

    response = client.post(
        "/auth/login",
        json={"email": "login_test@example.com", "password": "correctpassword"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    #проверяем что токен реально пришел в ответе
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
#проверяем что логин с неправильным паролем не проходит
    client.post(
        "/auth/register",
        json={"email": "wrongpass@example.com", "password": "correctpassword"},
    )

    response = client.post(
        "/auth/login",
        json={"email": "wrongpass@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == 401
    #ожидаем именно 401, которую мы настраивали для неверного пароля