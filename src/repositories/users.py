from typing import Any, Optional

from sqlalchemy.engine import Row

from ..data_sources.users import UserAdaptor
from sqlalchemy.orm import Session

from ..models.models import User


class UserRepository:
    adaptor = UserAdaptor

    @staticmethod
    def base_return(user: Optional[Row[Any]]):
        if not user:
            return None
        return user._mapping.get("User", user._mapping)

    async def get_and_create(
            self, name: str, last_name: str, phone_number: str, db_session: Session
    ):
        create_query = self.adaptor.create(name=name, last_name=last_name, phone_number=phone_number)
        async with db_session.begin() as session:
            session.add(create_query)
            await session.flush()
            query = self.adaptor.query_by_phone_number(phone_number)
            user = (await session.execute(query)).first()
        return UserRepository.base_return(user)

    async def get_by_phone_number(self, phone_number: str, db_session: Session):
        query = self.adaptor.get_by_phone_number(phone_number)
        async with db_session.begin() as session:
            user = (await session.execute(query)).first()
        return UserRepository.base_return(user)

    async def query_by_id(self, user_id: str, db_session: Session):
        query = self.adaptor.query_by_id(user_id)
        async with db_session.begin() as session:
            user = (await session.execute(query)).first()
        return UserRepository.base_return(user)
