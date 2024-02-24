from pydantic import BaseModel
from datetime import datetime
from fastapi import Body


class UserBase(BaseModel):
    name: str
    last_name: str
    phone_number: str = Body(regex="^09(1[0-9]|3[1-9])-?[0-9]{3}-?[0-9]{4}$")


class UserDisplay(BaseModel):
    name: str
    last_name: str
    phone_number: str

    class Config:
        from_attributes = True
