from fastapi import Depends, HTTPException, status
#Depends для зависимостей, HTTPException и status для ошибок авторизации
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
#HTTPBearer дает простое поле для токена в Swagger, без лишних полей формы
from sqlalchemy.orm import Session
#тип Session для аннотации
from app.core.database import get_db
#наша функция получения сессии
from app.repositories.user_repository import UserRepository
#репозиторий юзера
from app.repositories.task_repository import TaskRepository
#репозиторий задач
from app.services.user_service import UserService
#сервис юзера
from app.services.task_service import TaskService
#сервис задач
from app.services.auth_service import decode_access_token
#наша функция расшифровки токена
from app.models.user import User
#модель юзера
from app.repositories.habit_template_repository import HabitTemplateRepository
#репозиторий привычек
from app.services.habit_service import HabitService
#сервис привычек


def get_user_service(db: Session = Depends(get_db)) -> UserService:
#функция зависимость, собирает готовый UserService
    repository = UserRepository(db)
    return UserService(repository)


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
#функция зависимость, собирает готовый TaskService
    repository = TaskRepository(db)
    return TaskService(repository)


security = HTTPBearer()
#создаем схему авторизации через Bearer токен, дает простое поле в Swagger


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
        )

    repository = UserRepository(db)
    #создаем репозиторий вместо прямого обращения к db
    user = repository.get_user_by_id(int(user_id))
    #используем метод репозитория вместо db.query напрямую
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )

    return user

def get_habit_service(db: Session = Depends(get_db)) -> HabitService:
#функция зависимость, собирает готовый HabitService
    habit_repository = HabitTemplateRepository(db)
    task_repository = TaskRepository(db)
    #HabitService нужны оба репозитория, создаем их здесь
    return HabitService(habit_repository, task_repository)