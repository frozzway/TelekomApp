import cherrypy
from alembic import command

from app import controllers
from app.container import Container
from app.services import PrefillService
from app.settings import settings, alembic_cfg
from app import tools  # type: ignore[import]


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
    })

    config = {
        '/': {
            'tools.json_in.on': True,
            'tools.json_out.on': True,
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.pydantic_dump.on': True,
            'tools.auth_tool.on': True,
        }
    }

    cherrypy.tree.mount(controllers.EquipmentController(), '/api/equipment', config=config)
    cherrypy.tree.mount(controllers.EquipmentTypeController(), '/api/equipment-type', config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()


run_migrations()
container = Container()
container.init_resources()
container.wire(modules=[controllers])
prefill_data(container.prefill_service())
start_cherrypy()

