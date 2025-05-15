import cherrypy


@cherrypy.tools.register('on_start_resource')
def cors_tool():
    """Tool для установки CORS-заголовков в ответы сервера"""

    req = cherrypy.request
    resp = cherrypy.response

    origin = req.headers.get('Origin', '*')
    resp.headers['Access-Control-Allow-Origin'] = origin
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'

    if req.method == 'OPTIONS':
        cherrypy.response.status = 200

        def _preflight_response():
            return ''

        req.handler = _preflight_response
