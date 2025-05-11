import cherrypy
from dependency_injector.wiring import inject

from app.controllers.utils import make_model_paginated
from app.dependencies import EquipmentTypeServiceDp
from app.models import EquipmentTypeFilterDto
from app.models import EquipmentTypeVm
from app.models import PaginatedQueryResult


@cherrypy.expose
class EquipmentTypeController:
    """Контроллер для работы с сущностью 'Тип оборудования'"""

    @inject
    def GET(self, equipment_type_service: EquipmentTypeServiceDp, **kwargs) -> PaginatedQueryResult[EquipmentTypeVm]:
        dto = make_model_paginated(EquipmentTypeFilterDto, cherrypy.request.params)
        return equipment_type_service.get_entities(dto)
