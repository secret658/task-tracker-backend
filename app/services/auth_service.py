from passlib.context import CryptContext
#импортируем CryptContext, инструмент для хэширования и проверки паролей
from datetime import datetime, timedelta
#datetime для текущего времени, timedelta для расчета времени истечения токена
from jose import jwt
#jwt из библиотеки python-jose, для создания и проверки токенов
from app.core.config import settings
#импортируем settings, там лежит наш SECRET_KEY
from jose import JWTError, jwt
#JWTError это исключение, которое библиотека кинет если токен невалидный или истек

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#создаем объект настройки, говорим использовать алгоритм bcrypt
#deprecated="auto" нужен для будущего перехода на новый алгоритм без поломки старых хэшей


def hash_password(password: str) -> str:
#функция принимает сырой пароль строкой, возвращает хэш строкой
    return pwd_context.hash(password)
    #хэширует пароль через bcrypt и возвращает результат


def verify_password(plain_password: str, hashed_password: str) -> bool:
#функция принимает сырой пароль и хэш из базы, возвращает True или False
    return pwd_context.verify(plain_password, hashed_password)
    #сравнивает пароль с хэшем, хэшируя plain_password тем же способом
    #и проверяя совпадение результатов

def create_access_token(data: dict) -> str:
#функция принимает словарь с данными для токена, возвращает строку токена
    to_encode = data.copy()
    #копируем словарь, чтобы не изменить оригинальный объект снаружи функции
    expire = datetime.utcnow() + timedelta(minutes=30)
    #считаем время истечения токена, текущее время плюс 30 минут
    to_encode.update({"exp": expire})
    #добавляем в словарь поле exp, это стандартное поле JWT для времени истечения
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    #создаем и подписываем токен нашим секретным ключом, алгоритм HS256
    return encoded_jwt

def decode_access_token(token: str) -> dict | None:
#функция принимает строку токена, возвращает словарь с данными или None
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        #расшифровывает токен тем же секретным ключом и алгоритмом, которым подписывали
        return payload
        #возвращает словарь с данными, включая user_id и exp
    except JWTError:
        #ловим ошибку если токен подделан, истек срок, или искажен
        return None
        #возвращаем None, значит токен невалиден