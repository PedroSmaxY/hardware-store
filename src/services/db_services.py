from typing import Optional
from src.repository.repositories import UserRepository
from src.models.data_models import User


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, name: str, email: str, age: int) -> int:
        if not name or not email:
            raise ValueError("Name and email are required fields")

        if (age < 0 or age > 120):
            raise ValueError("Age must be between 0 and 120")

        return self.repository.create(name, email, age)

    def get_all_users(self) -> list[User]:
        return self.repository.find_all()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.repository.find_by_id(user_id)

    def update_user(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None, age: Optional[int] = None) -> bool:
        if age is not None and (age < 0 or age > 120):
            raise ValueError("Age must be between 0 and 120")

        return self.repository.update(user_id, name, email, age)

    def delete_user(self, user_id: int) -> bool:
        return self.repository.delete(user_id)
