from fastapi import APIRouter, Depends, HTTPException
#APIRouter для создания группы роутов, Depends для зависимостей, HTTPException для ошибок
from app.schemas.user import UserCreate, UserResponse
#схемы для регистрации и ответа
from app.services.user_service import UserService
#тип сервиса для аннотации
from app.api.dependencies import get_user_service
#наша функция-зависимость, которая соберет готовый сервис
from pydantic import BaseModel

router = APIRouter()
#создаем объект роутера, в него будем добавлять эндпоинты


@router.post("/register", response_model=UserResponse)
#POST запрос на /register, ответ будет сериализован по схеме UserResponse
def register(user_data: UserCreate, service: UserService = Depends(get_user_service)):
#принимает данные регистрации, получает готовый сервис через Depends
    try:
        new_user = service.register_user(user_data)
        #вызываем метод сервиса, вся логика уже там
        return new_user
        #возвращаем созданного юзера, FastAPI сам сконвертирует через UserResponse
    except ValueError as e:
    #ловим ошибку, которую кидает сервис если email уже занят
        raise HTTPException(status_code=400, detail=str(e))
        #превращаем в HTTP ошибку 400 с текстом сообщения

class LoginRequest(BaseModel):
#схема того, что юзер присылает при входе
    email: str
    password: str


class TokenResponse(BaseModel):
#схема ответа с токеном
    access_token: str
    token_type: str = "bearer"
    #token_type по умолчанию "bearer", это стандарт для JWT в заголовках


@router.post("/login", response_model=TokenResponse)
#POST запрос на /login, ответ в виде токена
def login(login_data: LoginRequest, service: UserService = Depends(get_user_service)):
#принимает email и пароль, получает готовый сервис
    try:
        token = service.authenticate_user(login_data.email, login_data.password)
        #вызываем метод сервиса, вся проверка пароля уже внутри
        return TokenResponse(access_token=token)
        #оборачиваем токен в схему ответа
    except ValueError as e:
    #ловим ошибку "неверный email или пароль"
        raise HTTPException(status_code=401, detail=str(e))
        #401 Unauthorized, а не 400 - это стандартный код именно для проблем с авторизацией