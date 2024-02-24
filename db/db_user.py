from db.database import Base
from schemas import UserBase
from sqlalchemy.orm import Session

User = Base.classes.user


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
