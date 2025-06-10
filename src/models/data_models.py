from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.config.db_config import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', age={self.age})>"
