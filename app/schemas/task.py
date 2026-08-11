from pydantic import BaseModel
#импортируем BaseModel из библиотеки Pydantic для создания схемы данных
from datetime import datetime, date
#datetime для времени создания и выполнения, date для task_date без времени


class TaskCreate(BaseModel):
#это схема данных для создания задачи, содержит одно поле title типа str (строка)
#не меняется, task_date/habit_template_id/completed_at заполняются сервисом
    title: str


class TaskResponse(BaseModel):
    id: int
    title: str
    is_done: bool
    created_at: datetime
    completed_at: datetime | None = None
    #новое поле, момент выполнения, None если задача еще не выполнена
    task_date: date
    #новое поле, к какому дню относится задача
    habit_template_id: int | None = None
    #новое поле, None если это разовая задача, иначе id шаблона привычки

    class Config:
        from_attributes = True


class HabitTemplateCreate(BaseModel):
#схема для создания нового шаблона привычки, только title
    title: str


class HabitTemplateResponse(BaseModel):
#схема ответа для шаблона привычки
    id: int
    title: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True