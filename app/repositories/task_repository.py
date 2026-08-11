from sqlalchemy.orm import Session
from app.models.task import Task


class TaskRepository:
#TaskRepository - это класс, который будет содержать методы для 
#работы с задачами в базе данных
    def __init__(self, db: Session):
    #__init__ - это метод инициализации класса, который принимает объект
    #Session из SQLAlchemy, который будет использоваться 
    #для работы с базой данных
        self.db = db
        #self.db - это атрибут класса, который будет содержать объект Session,
        #который будет использоваться для работы с базой данных
    def create_task(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task_by_id(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_tasks_by_user(self, user_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.user_id == user_id).all()

    def update_task(self, task: Task) -> Task:
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()

    def get_task_by_habit_and_date(self, habit_template_id: int, task_date) -> Task | None:
    #проверяет, существует ли уже задача для этой привычки на эту дату
        return (
        self.db.query(Task)
        .filter(Task.habit_template_id == habit_template_id, Task.task_date == task_date)
        .first()
    )

    def get_tasks_by_user_since(self, user_id: int, since_date) -> list[Task]:
        #получает все задачи юзера начиная с указанной даты
        return (
        self.db.query(Task)
        .filter(Task.user_id == user_id, Task.task_date >= since_date)
        .all()
    )