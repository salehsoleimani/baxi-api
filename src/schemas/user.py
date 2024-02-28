import datetime
from fastapi import Body
from pydantic import BaseModel


class UserQuery(BaseModel):
    id: int
    phone_number: str
    updated_at: datetime.datetime
    created_at: datetime.datetime


class UserIn(BaseModel):
    phone_number: str = Body(regex="((0?9)|(\+?989))\d{2}\W?\d{3}\W?\d{4}")
    otp_code: str


class UserOut(BaseModel):
    id: str
    updated_at: datetime.datetime
    created_at: datetime.datetime


class PhoneNumber(BaseModel):
    phone_number: str = Body(regex="((0?9)|(\+?989))\d{2}\W?\d{3}\W?\d{4}")
