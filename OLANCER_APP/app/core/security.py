from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    this method use to create access token
    :param subject: subject to use to encode ...
    :type subject: str
    :param expires_delta: the time to expire access token ...
    :type expires_delta: timedelta
    :return: encoded jwt
    :rtype: str
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    this method use to verify password
    :param plain_password: current password
    :type plain_password: str
    :param hashed_password: hashed password
    :type hashed_password:str
    :return: password verify or not
    :rtype: bool
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    this method convert current password to hash password
    :param password: password
    :type password: str
    :return: hash password
    :rtype: str
    """
    return pwd_context.hash(password)
