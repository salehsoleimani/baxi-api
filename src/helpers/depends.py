from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.helpers.exceptions import ForbiddenException
from src.repositories.jwt import JWTHandler

http_bearer = HTTPBearer()


async def get_current_user(
        request: Request, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    if credentials.scheme != "Bearer":
        raise ForbiddenException("Invalid Header")
    access_token = request.cookies.get("Access-Token")
    if not access_token:
        raise ForbiddenException("Access-Token is not provided")
    token = JWTHandler.decode(access_token)
    user_id = token.get("user_id")
    if not user_id:
        raise ForbiddenException("Invalid Access Token")
    csrf_token = JWTHandler.decode(credentials.credentials)
    if csrf_token.get("access_token") != access_token:
        raise ForbiddenException("Invalid CSRF Token")
    return user_id


async def get_current_user_with_refresh(
        request: Request, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    if credentials.scheme != "Bearer":
        raise ForbiddenException("Invalid Header")
    refresh_token = request.cookies.get("Refresh-Token")
    if not refresh_token:
        raise ForbiddenException("Refresh-Token is not provided")
    token = JWTHandler.decode(refresh_token)
    user_id = token.get("verify")
    if not user_id:
        raise ForbiddenException("Invalid Refresh Token")
    csrf_token = JWTHandler.decode(credentials.credentials)
    if csrf_token.get("refresh_token") != refresh_token:
        raise ForbiddenException("Invalid CSRF Token")
    return user_id

