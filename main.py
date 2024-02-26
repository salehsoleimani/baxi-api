import uvicorn as uvicorn
from fastapi import FastAPI

from src.config.config import settings
from src.routers.auth import router as auth_router

app = FastAPI(docs_url='/docs', )
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
