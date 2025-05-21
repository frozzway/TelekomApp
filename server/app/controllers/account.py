import cherrypy
from dependency_injector.wiring import inject

from app import models
from app.controllers.utils import make_model
from app.dependencies import AuthServiceDp


class AccountController:
    """Контроллер для авторизации пользователя"""

    @cherrypy.expose
    @inject
    def login(self, auth_service: AuthServiceDp, **kwargs) -> models.Token:
        """
        Метод авторизации пользователя по учетным данным

        :param auth_service: Сервис авторизации
        :return: Access и Refresh токены
        """

        dto = make_model(models.Login, cherrypy.request.json)
        return auth_service.login(
            email=dto.username,  # type: ignore
            password=dto.password,
            ip_address=cherrypy.request.remote.ip,
            user_agent=cherrypy.request.headers.get('User-Agent', ''))

    @cherrypy.expose
    @inject
    def refresh_session(self, auth_service: AuthServiceDp, **kwargs) -> models.Token:
        """
        Метод обновления сессии пользователя

        :param auth_service: Сервис авторизации
        :return: Access и Refresh токены новой сессии
        """

        return auth_service.refresh_token(
            ip_address=cherrypy.request.remote.ip,
            user_agent=cherrypy.request.headers.get('User-Agent', ''))

    @cherrypy.expose
    @inject
    def logout(self, auth_service: AuthServiceDp, **kwargs) -> None:
        """
        Метод выхода из системы

        :param auth_service: Сервис авторизации
        """

        auth_service.logout()
