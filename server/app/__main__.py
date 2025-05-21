import cherrypy
from alembic import command

from app import controllers
from app import tools  # type: ignore[import]
from app.container import container
from app.services import PrefillService
from app.settings import settings, alembic_cfg


def run_migrations():
    command.upgrade(config=alembic_cfg, revision='head')


def prefill_data(prefill_service: PrefillService):
    prefill_service.prefill_equipment_types()
    prefill_service.prefill_equipments()
    prefill_service.create_roles()
    prefill_service.prefill_users()


def start_cherrypy():
    cherrypy.config.update({
        'environment': settings.server_environment,
        'server.socket_host': settings.server_host,
        'server.socket_port': settings.server_port,
        'engine.autoreload.on': False,
        'tools.cors_tool.on': True,
        'tools.pydantic_dump.on': True,
        'tools.json_in.on': True,
        'tools.json_out.on': True,
        'tools.resources_shutdown.on': True,
        'error_page.default': tools.jsonify_error
    })

    rest_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.auth_tool.on': True,
        }
    }

    account_config = {
        '/': {
            'tools.json_in.on': False
        },
        '/login': {
            'tools.json_in.on': True
        }
    }

    cherrypy.tree.mount(controllers.EquipmentController(), '/api/equipment', config=rest_config)
    cherrypy.tree.mount(controllers.EquipmentTypeController(), '/api/equipment-type', config=rest_config)
    cherrypy.tree.mount(controllers.AccountController(), '/api/account', config=account_config)
    cherrypy.engine.start()
    cherrypy.engine.block()


run_migrations()
container.wire(modules=[controllers])
prefill_data(container.prefill_service())
container.shutdown_resources()
start_cherrypy()

