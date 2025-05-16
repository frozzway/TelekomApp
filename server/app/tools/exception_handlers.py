import json

import cherrypy


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