from typing import Optional

from pydantic import BaseModel


class RefreshToken(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access_token: Optional[str]
    refresh_token: str
    csrf_token: str