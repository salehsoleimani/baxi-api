from typing import Any, Optional

from sqlalchemy.engine import Row

from ..config.config import settings
from ..data_sources.users import UserAdaptor
from sqlalchemy.orm import Session

from ..database.redis_client import RedisManager
from ..helpers.exceptions import UserPendingVerificationError
from ..models.models import User


class AuthRepository:

    async def send_otp(self, phone_number, otp, redis_session: RedisManager):
        otp_session = await redis_session.get(phone_number)
        if otp_session and settings.OTP_EXPIRE_SECONDS - settings.OTP_RESEND_SECONDS > redis_session.ttl(phone_number):
            raise UserPendingVerificationError

        await redis_session.set(phone_number, otp, ex=settings.OTP_EXPIRE_SECONDS)
