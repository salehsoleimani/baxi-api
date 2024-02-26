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

    def get_and_create(
            self, name: str, last_name: str, phone_number: str, db_session: Session
    ):
        create_query = self.adaptor.create(name=name, last_name=last_name, phone_number=phone_number)
        db_session.begin()
        try:
            db_session.add(create_query)
            db_session.flush()
            query = self.adaptor.query_by_phone_number(phone_number)
            user = db_session.execute(query).first()
            db_session.commit()
        except:
            db_session.rollback()
            raise
        finally:
            db_session.close()
        return UserRepository.base_return(user)

    def get_by_phone_number(self, phone_number: str, db_session: Session):
        query = self.adaptor.get_by_phone_number(phone_number)
        db_session.begin()
        try:
            user = db_session.execute(query).first()
            db_session.commit()
        except:
            db_session.rollback()
            raise
        finally:
            db_session.close()
        return UserRepository.base_return(user)

    def query_by_id(self, user_id, db_session: Session):
        query = self.adaptor.query_by_id(user_id)
        db_session.begin()
        try:
            user = db_session.execute(query).first()
            db_session.commit()
        except:
            db_session.rollback()
            raise
        finally:
            db_session.close()
        return UserRepository.base_return(user)
