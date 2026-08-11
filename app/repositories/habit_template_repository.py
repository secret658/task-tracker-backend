from sqlalchemy.orm import Session
#тип Session для аннотации
from app.models.habit_template import HabitTemplate
#модель, с которой работает этот репозиторий


class HabitTemplateRepository:
    def __init__(self, db: Session):
    #конструктор, принимает сессию, сохраняет в self.db
        self.db = db

    def create_habit(self, habit: HabitTemplate) -> HabitTemplate:
    #создает новый шаблон привычки в базе
        self.db.add(habit)
        #добавляем объект в сессию ожидания
        self.db.commit()
        #физически сохраняем в базу
        self.db.refresh(habit)
        #перечитываем объект, чтобы получить сгенерированный id и created_at
        return habit

    def get_habits_by_user(self, user_id: int) -> list[HabitTemplate]:
    #получает все активные привычки конкретного юзера
        return (
            self.db.query(HabitTemplate)
            .filter(HabitTemplate.user_id == user_id, HabitTemplate.is_active == True)
            .all()
        )
        #фильтруем сразу по двум условиям через запятую внутри filter,
        #это равносильно SQL WHERE user_id = ... AND is_active = true

    def get_habit_by_id(self, habit_id: int) -> HabitTemplate | None:
    #получает один шаблон привычки по id, понадобится для проверок владения
        return self.db.query(HabitTemplate).filter(HabitTemplate.id == habit_id).first()