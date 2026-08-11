from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
#импортируем Base из database.py, чтобы наследоваться от него в модели
#импортируем из sqlalchemy Column и Integer, String для определения 
#столбцов в таблице

class User(Base):
    __tablename__ = "users"
    #определяем имя таблицы в базе данных, которая будет соответствовать
    #__tablename__ = "users" - имя таблицы в базе данных, 
    #которая будет соответствовать этой модели

    id = Column(Integer, primary_key=True, index=True)
    #primary_key=True - уникальный идентификатор для каждой строки
    #index=True - создает индекс для этого столбца, чтобы ускорить поиск по нему
    email = Column(String(255), unique=True, index=True, nullable=False)
    #unique=True - значение в этом столбце должно быть уникальным
    #nullable=False - значение в этом столбце не может быть пустым
    hashed_password = Column(String(255), nullable=False)
    #String - тип данных для столбца, в данном случае строка
    tasks = relationship("Task", back_populates="owner")
    #tasks - это атрибут, который будет содержать список задач,
    #которые принадлежат этому пользователю
    #back_populates="owner" - это аргумент, который указывает на
    #атрибут owner в модели Task, который будет содержать объект User
    #relationship - это функция, которая создает связь между двумя моделями,
    #в данном случае между User и Task
    habit_templates = relationship("HabitTemplate", back_populates="owner")
