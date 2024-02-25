import datetime

from pydantic import BaseModel


class UserQuery(BaseModel):
    phone: str
    updated_at: datetime.datetime
    created_at: datetime.datetime


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    updated_at: datetime.datetime
    created_at: datetime.datetime


class UserOutRegister(UserQuery):
    qr_img: str

