import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.helpers.response_logger import ResponseLoggerMiddleware
from src.routers import auth

app = FastAPI(docs_url='/docs')
app.include_router(auth.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
]

app.add_middleware(
    ResponseLoggerMiddleware
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=origins)
# app.add_middleware(ResponseLoggerMiddleware, allowed_hosts=origins)

# @app.get("/get-my-ip")
# async def get_my_ip(request: Request):
#     client_host = request.client.host
#     print({"Client IP": client_host})

app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run(
        host="0.0.0.0",
        port=4000,
        app="main:app",
        reload=True,
        loop="uvloop",
        workers=1,
    )
