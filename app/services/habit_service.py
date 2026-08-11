from datetime import datetime
#datetime для получения сегодняшней даты
from app.repositories.habit_template_repository import HabitTemplateRepository
#репозиторий шаблонов привычек
from app.repositories.task_repository import TaskRepository
#репозиторий задач, нужен для генерации задач-экземпляров
from app.models.habit_template import HabitTemplate
#модель шаблона привычки
from app.models.task import Task
#модель задачи
from app.schemas.task import HabitTemplateCreate
#схема создания привычки


class HabitService:
    def __init__(self, habit_repository: HabitTemplateRepository, task_repository: TaskRepository):
    #сервису нужны оба репозитория - привычек и задач, они будут работать вместе
        self.habit_repository = habit_repository
        self.task_repository = task_repository

    def create_habit(self, habit_data: HabitTemplateCreate, user_id: int) -> HabitTemplate:
    #создает только шаблон привычки, без генерации задач - это отдельная логика в ensure_today_tasks
        new_habit = HabitTemplate(
            title=habit_data.title,
            user_id=user_id,
            is_active=True,
        )
        #создаем объект модели привычки, is_active по умолчанию True
        return self.habit_repository.create_habit(new_habit)
        #сохраняем через репозиторий и возвращаем результат

    def ensure_today_tasks(self, user_id: int) -> None:
    #проверяет все активные привычки юзера, создает задачу на сегодня если её еще нет
        today = datetime.utcnow().date()
        #сегодняшняя дата без времени
        habits = self.habit_repository.get_habits_by_user(user_id)
        #все активные привычки юзера

        for habit in habits:
        #проходим по каждой активной привычке
            existing_task = self.task_repository.get_task_by_habit_and_date(habit.id, today)
            #проверяем, есть ли уже задача на сегодня для этой привычки
            if existing_task is None:
            #если задачи еще нет
                new_task = Task(
                    title=habit.title,
                    user_id=user_id,
                    habit_template_id=habit.id,
                    task_date=today,
                )
                self.task_repository.create_task(new_task)
                #создаем задачу на сегодня

    def get_user_habits(self, user_id: int) -> list[HabitTemplate]:
    #возвращает все активные привычки юзера
        return self.habit_repository.get_habits_by_user(user_id)