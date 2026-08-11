from app.repositories.user_repository import UserRepository
#импортируем репозиторий, сервис будет через него общаться с базой
from app.services.auth_service import hash_password, verify_password, create_access_token
#импортируем функцию хэширования пароля из auth_service
from app.models.user import User
#импортируем модель User, чтобы создавать объекты для сохранения в базу
from app.schemas.user import UserCreate
#импортируем схему, в которой приходят email и password от юзера


class UserService:
    def __init__(self, repository: UserRepository):
    #сервис принимает уже готовый репозиторий, а не сессию напрямую
        self.repository = repository
        #сохраняем репозиторий, чтобы методы класса могли им пользоваться

    def register_user(self, user_data: UserCreate) -> User:
    #принимает данные регистрации, возвращает созданного юзера
        existing_user = self.repository.get_user_by_email(user_data.email)
        #проверяем, не занят ли уже этот email
        if existing_user:
        #если юзер с таким email уже есть
            raise ValueError("Пользователь с таким email уже существует")
            #прерываем выполнение и кидаем ошибку, дальше код не пойдет

        hashed_password = hash_password(user_data.password)
        #хэшируем сырой пароль, полученный от юзера

        new_user = User(email=user_data.email, hashed_password=hashed_password)
        #создаем объект модели User с email и захэшированным паролем

        return self.repository.create_user(new_user)
        #сохраняем юзера через репозиторий и возвращаем результат

    def authenticate_user(self, email: str, password: str) -> str:
    #принимает email и пароль, возвращает JWT токен строкой
        user = self.repository.get_user_by_email(email)
        #ищем юзера по email
        if not user:
        #если юзер не найден
            raise ValueError("Неверный email или пароль")
            #та же ошибка что и для неверного пароля, из соображений безопасности

        if not verify_password(password, user.hashed_password):
        #сравниваем введенный пароль с хэшем из базы
            raise ValueError("Неверный email или пароль")
            #пароль не совпал, кидаем ту же ошибку

        access_token = create_access_token(data={"sub": str(user.id)})
        #создаем токен, кладем туда id юзера под стандартным ключом sub
        return access_token
        #возвращаем готовый токен