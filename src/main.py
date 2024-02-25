from fastapi import FastAPI
from src.database.database import Base
from src.database.database import engine
from src.routers import auth

app = FastAPI()
app.include_router(user.router)

Base.metadata.create_all(engine)
