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
        dto = make_model(models.Login, cherrypy.request.json)
        return auth_service.login(
            email=dto.username,  # type: ignore
            password=dto.password,
            ip_address=cherrypy.request.remote.ip,
            user_agent=cherrypy.request.headers.get('User-Agent', ''))

    @cherrypy.expose
    @inject
    def refresh_session(self, refresh_token: str, auth_service: AuthServiceDp, **kwargs) -> models.Token:
        return auth_service.refresh_token(
            refresh_token=refresh_token,
            ip_address=cherrypy.request.remote.ip,
            user_agent=cherrypy.request.headers.get('User-Agent', ''))