import cherrypy

from app.services import AuthService


@cherrypy.tools.register('on_start_resource')
def auth_tool(authorized_roles: list[str] | None = None) -> None:
    """
    Tool для проверки авторизации пользователя в системе

    :param authorized_roles: Роли, которыми ограничен доступ
    """

    auth_header: str = cherrypy.request.headers.get('Authorization', '')
    if not auth_header:
        raise AuthService.exception

    token = auth_header.replace('Bearer ', '')
    if token is None:
        raise AuthService.exception

    user = AuthService.verify_token(token)
    user_roles = set(user.roles)

    if authorized_roles and not any(authorized_role in user_roles for authorized_role in authorized_roles):
        raise AuthService.exception
