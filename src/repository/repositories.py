from typing import Optional
from src.config.db_config import Session
from src.models.data_models import User


class UserRepository:
    def create(self, name: str, email: str, age: int) -> int:
        session = Session()
        try:
            new_user = User(name=name, email=email, age=age)
            session.add(new_user)
            session.commit()
            user_id = new_user.id
            return user_id
        finally:
            session.close()

    def find_all(self) -> list[User]:
        session = Session()
        try:
            users = session.query(User).all()
            return users
        finally:
            session.close()

    def find_by_id(self, user_id: int) -> Optional[User]:
        session = Session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            return user
        finally:
            session.close()

    def update(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None, age: Optional[int] = None) -> bool:
        session = Session()
        try:
            user = session.query(User).filter(User.id == user_id).first()

            if user:
                if name:
                    user.name = name
                if email:
                    user.email = email
                if age is not None:
                    user.age = age

                session.commit()
                return True
            else:
                return False
        finally:
            session.close()

    def delete(self, user_id: int) -> bool:
        session = Session()
        try:
            user = session.query(User).filter(User.id == user_id).first()

            if user:
                session.delete(user)
                session.commit()
                return True
            else:
                return False
        finally:
            session.close()
