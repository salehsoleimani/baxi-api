from http.client import HTTPException

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

import schemas
from db.database import get_db
from db.models import User

routers = APIRouter(
    tags=['Authentication']
)


# @routers.post('/login', response_model=schemas.Token)
# def login(userdetails: OAuth2PasswordRequestForm, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == userdetails.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = f"The User Does not exist")
#     if not utils.verify_password(userdetails.password, user_password):
#         raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED  detail = "The Passwords do not match")
#
#     access_token = create_access_token(data={"user_id": user.id})
#     return {"access_token": access_token, "token_type": "bearer"}
