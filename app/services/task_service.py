from app.repositories.task_repository import TaskRepository
#импортируем репозиторий задач
from app.models.task import Task
#импортируем модель Task для создания объектов
from app.schemas.task import TaskCreate
#импортируем схему создания задачи
from datetime import datetime, timedelta

class TaskService:
    def __init__(self, repository: TaskRepository):
    #сервис принимает готовый репозиторий, как и UserService
        self.repository = repository
        #сохраняем репозиторий для использования в методах

    def create_task(self, task_data: TaskCreate, user_id: int) -> Task:
    #принимает данные задачи и id юзера отдельно, возвращает созданную задачу
        new_task = Task(title=task_data.title, user_id=user_id)
        #создаем объект модели, is_done и created_at подставятся по default
        return self.repository.create_task(new_task)
        #сохраняем через репозиторий и возвращаем результат

    def get_user_tasks(self, user_id: int) -> list[Task]:
        return self.repository.get_tasks_by_user(user_id)
    
    def complete_task(self, task_id: int, user_id: int) -> Task:
    #принимает id задачи и id юзера, возвращает обновленную задачу
        task = self.repository.get_task_by_id(task_id)
        #ищем задачу по id
        if not task:
        #если задача не найдена
            raise ValueError("Задача не найдена")
            #прерываем выполнение с ошибкой

        if task.user_id != user_id:
        #проверяем что задача принадлежит именно этому юзеру
            raise ValueError("Нет доступа к этой задаче")
            #если чужая задача, прерываем с ошибкой доступа

        task.is_done = True
        task.completed_at = datetime.utcnow()
        return self.repository.update_task(task)
        #сохраняем изменения через репозиторий и возвращаем результат

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.repository.get_task_by_id(task_id)
        if not task:
            raise ValueError("Задача не найдена")

        if task.user_id != user_id:
            raise ValueError("Нет доступа к этой задаче")

        self.repository.delete_task(task)

    def get_current_streak(self, user_id: int) -> int:
    #считает сколько дней подряд, начиная со вчера, все задачи были выполнены
        since_date = datetime.utcnow().date() - timedelta(days=90)
        #берем задачи за последние 90 дней, с запасом
        tasks = self.repository.get_tasks_by_user_since(user_id, since_date)
        #один запрос вместо цикла с запросами на каждый день

        tasks_by_date = {}
        #группируем задачи по дате в словарь
        for task in tasks:
            tasks_by_date.setdefault(task.task_date, []).append(task)
            #setdefault - если ключа еще нет, создает пустой список, потом добавляет task

        streak = 0
        current_date = datetime.utcnow().date() - timedelta(days=1)
        #начинаем со вчерашнего дня

        while True:
            day_tasks = tasks_by_date.get(current_date)
            #задачи за текущий проверяемый день, или None если их нет

            if not day_tasks:
            #если задач в этот день не было вообще
                break

            if not all(task.is_done for task in day_tasks):
            #проверяем что ВСЕ задачи в этот день выполнены
                break

            streak += 1
            current_date -= timedelta(days=1)

        return streak