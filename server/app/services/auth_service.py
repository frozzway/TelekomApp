from http import HTTPStatus

import bcrypt
from cherrypy import HTTPError
from jose import (
    JWTError,
    jwt,
)
from pydantic import ValidationError
from sqlalchemy.orm import Session

import app.models as models
from app.settings import settings


class AuthService:
    """Сервис авторизации"""

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password_byte_enc = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

    @staticmethod
    def hash_string(data: str) -> str:
        pwd_bytes = data.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_token(token: str) -> models.UserJWT:
        exception = HTTPError(
            status=HTTPStatus.UNAUTHORIZED,
            message='Could not validate credentials'
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = models.UserJWT.model_validate(user_data)
        except ValidationError:
            raise exception from None

        return user

