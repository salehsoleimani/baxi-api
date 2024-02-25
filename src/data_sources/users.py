import sqlalchemy as sa
from sqlalchemy import func

from src.models.models import User
from src.schemas.user import UserQuery


class UserAdaptor:
    @staticmethod
    def get_selects():
        return [getattr(User, field) for field in UserQuery.__fields__]

    @staticmethod
    def get_by_phone_number(phone_number: str):
        return sa.select(User).where(User.phone_number == phone_number)

    @staticmethod
    def get_by_id(user_id):
        return sa.select(User).where(User.id == user_id)

    @staticmethod
    def query_by_phone_number(phone_number: str):
        return sa.select(*UserAdaptor.get_selects()).where(User.phone_number.ilike(phone_number))

    @staticmethod
    def query_by_id(user_id):
        return sa.select(*UserAdaptor.get_selects()).where(User.id == user_id)

    @staticmethod
    def create(name: str, last_name: str, phone_number: str):
        return User(name=name, last_name=last_name, phone_number=phone_number)
