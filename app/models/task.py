from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey
from app.core.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
#импортируем Base из database.py, чтобы наследоваться от него в модели
#импортируем Column, Integer, String, Boolean, DateTime, ForeignKey из sqlalchemy 
#для определения столбцов в таблице

class Task(Base):
    __tablename__ = "tasks"
    #определяем имя таблицы в базе данных, которая будет соответствовать 
    #этой модели

    id = Column(Integer, primary_key = True, index=True)
    #primary_key=True - уникальный идентификатор для каждой строки
    #index=True - создает индекс для этого столбца, чтобы ускорить поиск по нему
    title = Column(String(255), index = True)
    is_done = Column(Boolean, default = False)
    created_at = Column(DateTime, default = datetime.utcnow)
    #default=datetime.utcnow - устанавливает текущее время как значение 
    #по умолчанию при создании новой задачи
    user_id = Column(Integer, ForeignKey("users.id"))
    #ForeignKey (внешний ключ) - значение должно обязательно существовать в 
    #другой таблице, в данном случае в таблице users, мы не сможем создать
    #id_user = 999 если его не суцществует в таблице users
    habit_template_id = Column(Integer, ForeignKey("habit_templates.id"), nullable=True)
    #новое поле, ссылка на шаблон привычки, пусто если это разовая задача
    task_date = Column(Date, nullable=False, default=datetime.utcnow)
    #новое поле, к какому дню относится эта задача
    owner = relationship("User", back_populates="tasks")
    habit_template = relationship("HabitTemplate")
    #связь с шаблоном привычки, без back_populates 
    #нам не нужен список задач со стороны шаблона прямо сейчас
    #owner - это атрибут, который будет содержать объект User, 
    #которому принадлежит эта задача
    #back_populates="tasks" - это аргумент, который указывает на
    #атрибут tasks в модели User, который будет содержать список задач
    #relationship - это функция, которая создает связь между двумя моделями,
    #в данном случае между Task и User, чтобы мы могли получить доступ 
    #к пользователю, которому принадлежит задача