from typing import Optional, Any

from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_sources.users import UserAdaptor


class UserRepository:
    adaptor = UserAdaptor

    @staticmethod
    def base_return(user: Optional[Row[Any]]):
        if not user:
            return None
        return user._mapping.get("User", user._mapping)

    async def get_and_create(
            self, name: str, last_name: str, phone_number: str, db_session: AsyncSession
    ):
        create_query = self.adaptor.create(name=name, last_name=last_name, phone_number=phone_number)
        async with db_session.begin():
            db_session.add(create_query)
            await db_session.flush()
            query = self.adaptor.query_by_phone_number(phone_number)
            user = (await db_session.execute(query)).first()
        return UserRepository.base_return(user)

    async def get_by_phone_number(self, phone_number: str, db_session: AsyncSession):
        query = self.adaptor.get_by_phone_number(phone_number)
        async with db_session.begin():
            user = (await db_session.execute(query)).first()
        return UserRepository.base_return(user)

    async def query_by_id(self, user_id, db_session: AsyncSession):
        query = self.adaptor.query_by_id(user_id)
        async with db_session.begin():
            user = (await db_session.execute(query)).first()
        return UserRepository.base_return(user)
