import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime

from src.database.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    last_name = Column(String(255), nullable=False, unique=True)
    phone_number = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=sqlalchemy.func.now())
    updated_at = Column(DateTime, nullable=False, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())
