import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.config import settings
from src.routers.auth import router as auth_router

app = FastAPI(docs_url='/docs', )
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(
        host="0.0.0.0",
        port=settings.port,
        app="main:app",
        reload=True,
        loop="uvloop",
        workers=1,
    )
