import asyncio
from http import HTTPStatus
from fastapi import HTTPException
from typing import Optional
from redis.asyncio.client import Redis
from sqlalchemy.orm import Session
from ..config.config import settings

from ..helpers.exceptions import BadRequestException, CustomException, UnauthorizedException, \
    UserPendingVerificationError
from ..helpers.sms_ir import sms_helper
from ..repositories.jwt import JWTHandler
from ..repositories.users import UserRepository
from ..schemas.auth import Token
from ..schemas.user import UserOut, UserQuery


class AuthController:
    user_repository = UserRepository()
    jwt_handler = JWTHandler

    def __init__(
            self,
            db_session: Session,
            redis_session: Optional[Redis] = None,
            user_repository: Optional[UserRepository] = None,
    ):
        self.user_repository = user_repository or self.user_repository
        self.db_session = db_session
        self.redis_session = redis_session

    async def send_otp(self, phone_number: str, otp_code: str) -> UserQuery:
        if not self.redis_session:
            raise CustomException("redis connection is not initialized")

        try:
            otp_session = await self.redis_session.get(phone_number)
            ttl = await self.redis_session.ttl(phone_number)
            if otp_session and settings.OTP_EXPIRE_SECONDS - settings.OTP_RESEND_SECONDS > ttl:
                raise UserPendingVerificationError

            await self.redis_session.set(phone_number, otp_code, ex=settings.OTP_EXPIRE_SECONDS)

            sms_helper.send_verify_code(
                number=phone_number,
                template_id=400106,
                parameters=[
                    {
                        "name": "code",
                        "value": otp_code,
                    },
                ],
            )
        except UserPendingVerificationError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="already exists a pending verification",
            )

    async def register(self, name: str, last_name: str, phone_number: str) -> UserQuery:
        user = await self.user_repository.get_by_phone_number(phone_number, db_session=self.db_session)

        if user:
            raise BadRequestException("User already exists with this phone number")

        user = await self.user_repository.get_and_create(
            name=name,
            last_name=last_name,
            phone_number=phone_number,
            db_session=self.db_session,
        )
        assert user is not None
        return UserQuery(
            phone_number=user.phone_number,
            updated_at=user.updated_at,
            created_at=user.created_at,
        )

    async def login(self, phone_number: str) -> Token:
        if not self.redis_session:
            raise CustomException("Redis connection is not initialized")

        user = await self.user_repository.get_by_phone_number(phone_number, db_session=self.db_session)
        otp = await self.redis_session.get(phone_number)
        print(user)
        # if (not user) or #todo: check otp
        if not user:
            raise BadRequestException("Invalid credentials")

        refresh_token = self.jwt_handler.encode_refresh_token(
            payload={"sub": "refresh_token", "verify": str(user.id)}
        )
        csrf_token = self.jwt_handler.encode_refresh_token(
            payload={
                "sub": "csrf_token",
                "refresh_token": str(refresh_token),
            }
        )
        await self.redis_session.set(
            name=refresh_token, value=user.id, ex=self.jwt_handler.refresh_token_expire
        )
        return Token(
            access_token=None,
            refresh_token=refresh_token,
            csrf_token=csrf_token,
        )

    async def logout(self, refresh_token) -> None:
        if not refresh_token:
            raise BadRequestException
        if not self.redis_session:
            raise CustomException("Database connection is not initialized")
        await self.redis_session.delete(refresh_token)
        return None

    async def me(self, user_id) -> UserOut:
        user = await self.user_repository.query_by_id(user_id, db_session=self.db_session)
        if not user:
            raise BadRequestException("Invalid credentials")
        return UserOut(
            username=user.username, updated_at=user.updated_at, created_at=user.created_at
        )

    async def verify(
            self,
            refresh_token: str,
            session_id: str,
            code: str,
            settings=settings,
    ) -> None:
        if not self.redis_session:
            raise CustomException("Database connection is not initialized")
        session_id_redis, user_id = await asyncio.gather(
            self.redis_session.get(session_id), self.redis_session.get(refresh_token)
        )
        if not user_id or len(str(user_id)) < 5:
            raise UnauthorizedException("Invalid Refresh Token")
        elif session_id_redis != user_id:
            user = await self.user_repository.query_by_id(user_id, db_session=self.db_session)
            assert user is not None
            # if not totp.TOTP(user.gauth).verify(code):
            #     raise BadRequestException("Invalid Code")
            print(user_id)
            await self.redis_session.set(
                session_id, value=user_id, ex=(settings.SESSION_EXPIRE_MINUTES) * 60
            )
        else:
            raise BadRequestException("Already Verified")
        return None

    async def refresh_token(self, old_refresh_token: str) -> Token:
        if not self.redis_session:
            raise CustomException("Database connection is not initialized")

        user_id, ttl, session_id = await asyncio.gather(
            self.redis_session.get(old_refresh_token),
            self.redis_session.ttl(old_refresh_token),
        )
        if not user_id:
            raise UnauthorizedException("Invalid Refresh Token")

        access_token = self.jwt_handler.encode(payload={"user_id": str(user_id)})
        refresh_token = self.jwt_handler.encode_refresh_token(
            payload={"sub": "refresh_token", "verify": str(user_id)}
        )
        csrf_token = self.jwt_handler.encode_refresh_token(
            payload={
                "sub": "csrf_token",
                "refresh_token": str(refresh_token),
                "access_token": str(access_token),
            }
        )
        await asyncio.gather(
            self.redis_session.set(refresh_token, user_id, ex=ttl),
            self.redis_session.delete(old_refresh_token),
        )
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            csrf_token=csrf_token,
        )
