import pytest
#основная библиотека тестирования
from fastapi.testclient import TestClient
#позволяет отправлять тестовые HTTP-запросы к приложению без реального сервера
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#нужны для создания отдельной тестовой базы
from sqlalchemy.pool import StaticPool

from app.main import app
#наше реальное приложение FastAPI
from app.core.database import Base, get_db
#Base для создания тестовых таблиц, get_db чтобы подменить его на тестовую версию


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
#специальная строка подключения - база данных прямо в оперативной памяти, не на диске
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
#connect_args нужен специально для SQLite, чтобы разрешить работу из разных потоков
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#своя тестовая фабрика сессий, отдельная от боевой


def override_get_db():
#функция-замена для get_db, будет использоваться вместо реальной во время тестов
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
#говорим FastAPI - везде где ожидается get_db, подставляй override_get_db вместо него


@pytest.fixture()
def client():
#fixture - готовая переиспользуемая заготовка, которую можно запрашивать в тестах
    Base.metadata.create_all(bind=engine)
    #создаем все таблицы в тестовой базе перед тестом
    yield TestClient(app)
    #отдаем тестовый клиент, тесты будут через него делать запросы
    Base.metadata.drop_all(bind=engine)
    #удаляем все таблицы после теста, чтобы следующий тест начинался с чистого листа