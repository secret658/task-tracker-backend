from fastapi import APIRouter, Depends, HTTPException
#стандартные импорты для роутера, зависимостей и ошибок
from app.schemas.task import TaskCreate, TaskResponse
#схемы создания и ответа для задач
from app.services.task_service import TaskService
#тип сервиса для аннотации
from app.api.dependencies import get_task_service, get_current_user, get_habit_service
#наши зависимости - сборка сервиса и получение текущего юзера
from app.models.user import User
#модель юзера, нужна для типизации current_user
from app.services.habit_service import HabitService

router = APIRouter()
#создаем роутер для задач


@router.post("/", response_model=TaskResponse)
#POST на /tasks (полный путь соберется в main.py через префикс)
def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service),
    #получаем готовый сервис задач
    current_user: User = Depends(get_current_user),
    #получаем текущего юзера из токена, а не из тела запроса
):
    new_task = service.create_task(task_data, current_user.id)
    #передаем данные задачи и id юзера, взятый из токена, а не от юзера напрямую
    return new_task


@router.get("/", response_model=list[TaskResponse])
def get_my_tasks(
    service: TaskService = Depends(get_task_service),
    habit_service: HabitService = Depends(get_habit_service),
    #добавили habit_service
    current_user: User = Depends(get_current_user),
):
    habit_service.ensure_today_tasks(current_user.id)
    #перед отдачей списка проверяем/создаем задачи на сегодня по привычкам
    tasks = service.get_user_tasks(current_user.id)
    return tasks


@router.patch("/{task_id}/complete", response_model=TaskResponse)
#PATCH на /tasks/{id}/complete, task_id берется из самого URL
def complete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
):
    try:
        updated_task = service.complete_task(task_id, current_user.id)
        #сервис сам проверит существование задачи и что она принадлежит юзеру
        return updated_task
    except ValueError as e:
    #ловим ошибки "не найдена" или "нет доступа" из сервиса
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{task_id}", status_code=204)
#DELETE на /tasks/{id}, 204 - стандартный код для успешного удаления без тела ответа
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
):
    try:
        service.delete_task(task_id, current_user.id)
        #сервис сам проверит существование и владение
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/streak")
#GET на /tasks/streak, отдельный путь для получения текущего стрика
def get_streak(
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
):
    streak = service.get_current_streak(current_user.id)
    #вызываем метод сервиса, вся логика подсчета уже там
    return {"streak": streak}
    #возвращаем простой словарь, FastAPI сам превратит его в JSON