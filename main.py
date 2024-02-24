from fastapi import FastAPI
from db.database import Base
from db.database import engine
from routers import user

app = FastAPI()
app.include_router(user.router)

Base.metadata.create_all(engine)
