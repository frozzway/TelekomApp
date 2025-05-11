import cherrypy
from pydantic import BaseModel


@cherrypy.tools.register('before_handler', priority=10)
def pydantic_dump():
    """Tool для преобразования модели pydantic, возвращенной обработчиком, в словарь"""

    handler = cherrypy.request.handler
    if handler:
        original_handler = handler

        def new_handler(*args, **kwargs):
            response = original_handler(*args, **kwargs)
            return modify_response(response)

        cherrypy.request.handler = new_handler


def modify_response(response):
    if isinstance(response, (list, tuple)):
        response = [
            item.model_dump() if isinstance(item, BaseModel) else item
            for item in response
        ]
    elif isinstance(response, BaseModel):
        response = response.model_dump()
    return response