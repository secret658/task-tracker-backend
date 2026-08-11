from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
#те же типы, что использовали в Task
from sqlalchemy.orm import relationship
#для связи с User и с задачами-экземплярами
from datetime import datetime
#для default значения created_at
from app.core.database import Base
#наследуемся от того же Base, что и остальные модели


class HabitTemplate(Base):
    __tablename__ = "habit_templates"
    #имя таблицы в базе, во множественном числе как договаривались

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    #название привычки, обязательное поле
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    #чей это шаблон, обязательная связь с юзером
    is_active = Column(Boolean, default=True)
    #можно выключить привычку, не удаляя историю
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="habit_templates")
    #связь с юзером, аналогично Task