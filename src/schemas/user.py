import datetime
from fastapi import Body
from pydantic import BaseModel


class UserQuery(BaseModel):
    phone_number: str
    updated_at: datetime.datetime
    created_at: datetime.datetime


class UserIn(BaseModel):
    name: str
    last_name: str
    phone_number: str = Body(regex="^09(1[0-9]|3[1-9])-?[0-9]{3}-?[0-9]{4}$")


class UserOut(BaseModel):
    username: str
    updated_at: datetime.datetime
    created_at: datetime.datetime


class PhoneNumber(BaseModel):
    phone_number: str = Body(regex="^09(1[0-9]|3[1-9])-?[0-9]{3}-?[0-9]{4}$")
