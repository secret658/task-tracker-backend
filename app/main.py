from fastapi import FastAPI
#импортируем класс FastAPI, из него создается всё приложение
from app.api.routes import auth, tasks
#импортируем файлы с роутами auth и tasks
from app.core.database import Base, engine
#Base нужен чтобы создать таблицы, engine чтобы к чему подключаться
from app.api.routes import auth, tasks, habits
#добавили habits к существующему импорту
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)
#создает все таблицы в базе данных, если их еще нет
#смотрит на все модели, которые наследуются от Base

app = FastAPI(title="ТАСК ТРЕК API")
#создаем сам объект приложения, title просто для документации

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
#подключаем роуты регистрации/логина, все пути будут начинаться с /auth
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
#подключаем роуты задач, все пути будут начинаться с /tasks

app.include_router(habits.router, prefix="/habits", tags=["habits"])
#добавили после существующих include_router
