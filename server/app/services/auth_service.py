from datetime import datetime, timedelta
from http import HTTPStatus
import secrets

import bcrypt
import cherrypy
from cherrypy import HTTPError
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session, scoped_session

import app.models as models
import app.tables as tables
from app.settings import settings, timezone


class AuthService:
    """Сервис авторизации"""

    exception = HTTPError(status=HTTPStatus.UNAUTHORIZED, message='Could not validate credentials')

    def __init__(self, session: scoped_session[Session]):
        self.session = session()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password_byte_enc = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

    @staticmethod
    def hash_string(data: str, random_salt: bool = True) -> str:
        pwd_bytes = data.encode('utf-8')
        salt = bcrypt.gensalt() if random_salt else settings.bcrypt_salt
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_token(token: str) -> models.UserJWT:
        """
        Валидировать Access токен и извлечь из него данные о пользователе

        :param token: Access токен
        :return: Модель отображения пользователя
        """

        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise AuthService.exception from None

        user_data = payload.get('user')

        try:
            user_vm = models.UserJWT.model_validate(user_data)
        except ValidationError:
            raise AuthService.exception from None

        return user_vm

    @staticmethod
    def create_tokens(user: tables.User) -> models.Token:
        """
        Выпустить Access и Refresh токены для пользователя

        :param user: пользователь
        :return: Модель отображения с Access и Refresh токенами
        """

        user_data = models.UserJWT(
            id=user.id,
            roles=[r.name for r in user.roles])
        now = datetime.now(timezone)
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_s),
            'sub': str(user_data.id),
            'user': user_data.model_dump(mode='json'),
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return models.Token(access_token=token, refresh_token=secrets.token_hex(32))

    def get_refresh_session(self, hashed_token: str) -> tables.RefreshSession:
        """
        Получить сущность "Сессия для обновления JWT"

        :param hashed_token: хэшированное значение Refresh токена
        :return: Сущность "Сессия для обновления JWT"
        """

        return self.session.scalar(
            select(tables.RefreshSession)
            .where(
                tables.RefreshSession.token_hash == hashed_token,
                tables.RefreshSession.expires_in >= func.now()))

    def login(self, email: str, password: str, ip_address: str, user_agent: str) -> models.Token:
        """
        Авторизовать пользователя по учетным данным

        :param email: почтовый адрес
        :param password: пароль
        :param ip_address: ip адрес из запроса
        :param user_agent: юзер-агент из запроса
        :return: Модель отображения с Access и Refresh токенами
        """

        stmt = select(tables.User) \
            .where((tables.User.email == email) & (tables.User.is_deleted.is_(False)))
        user = self.session.scalars(stmt).one_or_none()

        if not user or not self.verify_password(password, user.hashed_password):
            raise self.exception

        tokens = self.create_tokens(user)
        refresh_session = self._create_refresh_session(tokens.refresh_token, user.id, ip_address, user_agent)
        self.session.add(refresh_session)
        self.session.commit()
        self._set_refresh_token(tokens.refresh_token)
        return tokens

    def _get_refresh_token(self) -> str:
        """
        Получить Refresh Token из cookie
        :return: Refresh Token
        """

        if cookie := cherrypy.request.cookie.get(settings.jwt_cookie_name):
            return cookie.value
        raise self.exception

    @staticmethod
    def _set_refresh_token(token: str | None) -> None:
        """
        Установить Refresh Token в cookie
        :param token: Значение токена
        """

        cherrypy.response.cookie[settings.jwt_cookie_name] = token
        cherrypy.response.cookie[settings.jwt_cookie_name]['httponly'] = True
        cherrypy.response.cookie[settings.jwt_cookie_name]['secure'] = True
        cherrypy.response.cookie[settings.jwt_cookie_name]['path'] = '/'
        cherrypy.response.cookie[settings.jwt_cookie_name]['samesite'] = 'Strict'
        cherrypy.response.cookie[settings.jwt_cookie_name]['expires'] = settings.jwt_refresh_token_expires_s

    def _get_refresh_session(self) -> tables.RefreshSession:
        """Получить сущность 'Сессия для обновления JWT' по токену из cookie"""

        refresh_token = self._get_refresh_token()
        hashed_token = self.hash_string(refresh_token, random_salt=False)
        refresh_session = self.get_refresh_session(hashed_token)
        if not refresh_session:
            raise HTTPError(status=HTTPStatus.UNAUTHORIZED, message='Token expired or invalid')
        return refresh_session

    def logout(self) -> None:
        """Удалить сессию из базы и очистить Refresh токен из cookie"""

        refresh_session = self._get_refresh_session()
        self.session.delete(refresh_session)
        self.session.commit()
        self._set_refresh_token(None)

    def refresh_token(self, ip_address: str, user_agent: str) -> models.Token:
        """
        Обновить сессию, выпустив новый Access токен и заменив Refresh

        :param ip_address: ip адрес из запроса
        :param user_agent: юзер-агент из запроса
        :return: Модель отображения с Access и Refresh токенами
        """
        refresh_session = self._get_refresh_session()
        user_id = refresh_session.user_id
        self._remove_expired_sessions(user_id)
        self.session.delete(refresh_session)
        user = self.session.scalar(select(tables.User).where(tables.User.id == user_id, tables.User.is_deleted.is_(False)))
        new_tokens = self.create_tokens(user)
        new_refresh_session = self._create_refresh_session(new_tokens.refresh_token, user_id, ip_address, user_agent)
        self.session.add(new_refresh_session)
        self.session.commit()
        self._set_refresh_token(new_tokens.refresh_token)
        return new_tokens

    def _remove_expired_sessions(self, user_id: int) -> None:
        """
        Удалить из базы все сессии с истекшим сроком жизни для пользователя

        :param user_id: Идентификатор пользователя
        """

        self.session.execute(
            delete(tables.RefreshSession)
            .where(
                tables.RefreshSession.user_id == user_id,
                tables.RefreshSession.expires_in < func.now()))

    def _create_refresh_session(self, refresh_token: str,
                                user_id: int, ip_address: str, user_agent: str) -> tables.RefreshSession:
        """
        Создать сущность "Сессия для обновления JWT" для пользователя

        :param refresh_token: Токен Refresh для выпуска Access
        :param user_id: идентификатор пользователя
        :param ip_address: ip адрес из запроса
        :param user_agent: юзер-агент из запроса
        :return: Сущность "Сессия для обновления JWT"
        """

        now = datetime.now(timezone)
        return tables.RefreshSession(
            user_id=user_id,
            token_hash=self.hash_string(refresh_token, random_salt=False),
            created_at=now,
            expires_in=now + timedelta(seconds=settings.jwt_refresh_token_expires_s),
            ip_address=ip_address,
            user_agent=user_agent)

