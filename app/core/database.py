from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
#app.core.config это работает благодаря тому что у тебя везде лежат 
#файлы __init__.py, которые превращают папки в пакеты (packages), 
#которые можно импортировать через точку.

engine = create_engine(settings.database_url)
#пул подкеключений чтобы не тратить лишнее время

Base = declarative_base()
#класс родитель для будущих моделей, чтобы не писать в каждой модели 
#одинаковый код

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#по вызову SessionLocal() создается новая сессия

#источник свежей сессии на каждый отдельный запрос
def get_db():
#обычная функция которая становиться генератором изза yield,
    db = SessionLocal()
    #вызываемс фабрику сессий и создаем новую сессию
    try:
        yield db
        #yield отдает сессию db тому кт оее вызвал
    finally:
        db.close()
        #ВСЕГДА закрывает бд