import json

import cherrypy

from app.container import container


def jsonify_error(status: str, message: str, traceback: str, version: str) -> str:
    """
    Формирует JSON-ответ для ошибки HTTP, совместимый с обработчиком `error_page` CherryPy.

    Args:
        status: HTTP-статус (например, '404 Not Found').
        message: Сообщение об ошибке, переданное в исключении.
        traceback: Стек вызовов ошибки (может быть None, если отключено).
        version: Версия CherryPy (например, 'CherryPy/18.8.0').

    Returns:
        JSON-строка, представляющая ошибку.
    """

    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.response.status = status

    try:
        message = json.loads(message)
    except json.decoder.JSONDecodeError:
        pass

    return json.dumps({
        'status': status,
        'error': message,
    })


@cherrypy.tools.register('before_handler', priority=20)
def resources_shutdown():
    """Tool для завершения работы всех ресурсов в случае возникновения исключения на обработчике запроса"""

    handler = cherrypy.request.handler
    if handler:
        original_handler = handler

        def wrapper(*args, **kwargs):
            try:
                return original_handler(*args, **kwargs)
            finally:
                container.shutdown_resources()

        cherrypy.request.handler = wrapper
