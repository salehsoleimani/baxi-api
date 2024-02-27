import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

app = FastAPI(docs_url='/docs')


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=origins)

@app.get("/get-my-ip")
async def get_my_ip(request: Request):
    client_host = request.client.host
    print({"Client IP": client_host})

if __name__ == "__main__":
    uvicorn.run(
        host="0.0.0.0",
        port=4000,
        app="main:app",
        reload=True,
        loop="uvloop",
        workers=1,
    )