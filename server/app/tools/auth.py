import cherrypy

from app.services import AuthService


@cherrypy.tools.register('on_start_resource')
def auth_tool():
    """Tool для проверки авторизации пользователя в системе"""

    auth_header: str = cherrypy.request.headers.get('Authorization', '')
    if not auth_header:
        raise AuthService.exception

    token = auth_header.replace('Bearer ', '')
    if token is None:
        raise AuthService.exception

    AuthService.verify_token(token)
