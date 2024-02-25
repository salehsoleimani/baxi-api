from db.database import Base
from db.models import User
from schemas import UserBase
from sqlalchemy.orm import Session


def create_user(request: UserBase, db: Session):
    user = User(
        name=request.name,
        last_name=request.last_name,
        phone_number=request.phone_number,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
