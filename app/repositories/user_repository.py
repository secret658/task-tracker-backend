from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
    #эта функция получает пользователя по его email. 
    #Она использует метод query объекта Session для выполнения 
    #запроса к базе данных, фильтруя результаты по полю email 
    #модели User. Если пользователь с указанным email найден, 
    #возвращается объект User, иначе возвращается None.

    def get_user_by_id(self, user_id: int) -> User | None:
#принимает id юзера, возвращает объект User или None если не найден
        return self.db.query(User).filter(User.id == user_id).first()
        #та же логика что get_user_by_email, просто фильтр по id вместо email