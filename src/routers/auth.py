import asyncio
import random
import string
import time
from fastapi import APIRouter, Depends, Request, Response, Form
from sqlalchemy.orm import Session
from src.controllers.auth import AuthController
from src.database.database import get_db
from redis.asyncio.client import Redis
from src.database.redis_client import get_redis
from src.helpers.depends import get_current_user_with_refresh, get_current_user
from src.schemas.user import UserIn, UserOut, PhoneNumber

router = APIRouter(
    prefix="/api/auth",
    tags=[
        "auth",
    ],
)


@router.post("/otp")
async def phone_number(phone: PhoneNumber, db_session: Session = Depends(get_db),
                       redis_session: Redis = Depends(get_redis)):
    otp_code = ''.join(random.choice(string.digits) for _ in range(4))
    return await AuthController(db_session=db_session, redis_session=redis_session).send_otp(phone.phone_number,
                                                                                             otp_code)


@router.post("/login")
async def login(
        data: UserIn,
        response: Response,
        db_session: Session = Depends(get_db),
        redis_db: Redis = Depends(get_redis),
):
    # rate limit code
    start_time = time.time()
    try:
        tokens = await AuthController(db_session=db_session, redis_session=redis_db).login(
            **data.dict()
        )
        elapsed_time = time.time() - start_time
        if elapsed_time < 1:
            await asyncio.sleep(1 - elapsed_time)
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time < 1:
            await asyncio.sleep(1 - elapsed_time)
        raise e from None

    response.set_cookie(
        key="Refresh-Token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="strict",
    )
    response.headers["X-CSRF-TOKEN"] = tokens.csrf_token


@router.post("/refresh")
async def refresh_token(
        response: Response,
        request: Request,
        csrf_token: str = Form(...),
        db_session: Session = Depends(get_db),
        redis_db: Redis = Depends(get_redis),
):
    start_time = time.time()
    try:
        tokens = await AuthController(db_session=db_session, redis_session=redis_db).refresh_token(
            old_refresh_token=request.cookies.get("Refresh-Token", ""),
            csrf_token=csrf_token
        )
        elapsed_time = time.time() - start_time
        if elapsed_time < 1:
            await asyncio.sleep(1 - elapsed_time)
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time < 1:
            await asyncio.sleep(1 - elapsed_time)
        raise e from None

    response.set_cookie(
        key="Refresh-Token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="strict",
    )
    response.set_cookie(
        key="Access-Token",
        value=tokens.access_token,
        secure=True,
        httponly=True,
        samesite="strict",
    )
    response.headers["X-CSRF-TOKEN"] = tokens.csrf_token
    return None


@router.get("/me")
async def me(current_user: UserOut = Depends(get_current_user)):
    return current_user


@router.delete("/logout")
async def logout(
        response: Response,
        request: Request,
        redis_db: Redis = Depends(get_redis),
):
    await AuthController(redis_session=redis_db, db_session=None).logout(
        request.cookies.get("Refresh-Token", ""),
    )
    response.set_cookie(
        key="Refresh-Token",
        value="",
        secure=True,
        httponly=True,
        samesite="strict",
    )
    response.set_cookie(
        key="Access-Token",
        value="",
        secure=True,
        httponly=True,
        samesite="strict",
    )
    return None
