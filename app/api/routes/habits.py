from fastapi import APIRouter, Depends, HTTPException
#стандартные импорты
from app.schemas.task import HabitTemplateCreate, HabitTemplateResponse
#схемы создания и ответа для привычек
from app.services.habit_service import HabitService
#тип сервиса для аннотации
from app.api.dependencies import get_habit_service, get_current_user
#зависимости - сборка сервиса и получение текущего юзера
from app.models.user import User
#модель юзера для типизации

router = APIRouter()
#создаем роутер для привычек


@router.post("/", response_model=HabitTemplateResponse)
#POST на /habits, полный путь соберется в main.py через префикс
def create_habit(
    habit_data: HabitTemplateCreate,
    service: HabitService = Depends(get_habit_service),
    current_user: User = Depends(get_current_user),
):
    new_habit = service.create_habit(habit_data, current_user.id)
    #создаем шаблон привычки, id юзера берем из токена, не из тела запроса
    return new_habit

@router.get("/", response_model=list[HabitTemplateResponse])
#GET на /habits, возвращает список активных привычек юзера
def get_habits(
    service: HabitService = Depends(get_habit_service),
    current_user: User = Depends(get_current_user),
):
    habits = service.get_user_habits(current_user.id)
    return habits