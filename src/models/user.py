from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class User(Base):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(unique=True, default=None)
    last_name: Mapped[str] = mapped_column(unique=True, default=None)
    phone_number: Mapped[str] = mapped_column(default=None)