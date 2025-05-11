import cherrypy
from dependency_injector.wiring import inject

from app.controllers.utils import make_model
from app.controllers.utils import make_model_paginated
from app.dependencies import EquipmentServiceDp
from app.models import EquipmentCreateDto
from app.models import EquipmentUpdateDto
from app.models import EquipmentCreateResult
from app.models import EquipmentFilterDto
from app.models import EquipmentGridVm
from app.models import EquipmentVm
from app.models import PaginatedQueryResult


@cherrypy.expose
class EquipmentController:
    """Контроллер для работы с сущностью 'Оборудование'"""

    @inject
    def POST(self, equipment_service: EquipmentServiceDp, **kwargs) -> EquipmentCreateResult:
        dto = make_model(EquipmentCreateDto, cherrypy.request.json)
        return equipment_service.create_equipments(dto)

    @inject
    def GET(self, equipment_id: str = None, *, equipment_service: EquipmentServiceDp, **kwargs
            ) -> PaginatedQueryResult[EquipmentGridVm] | EquipmentVm:
        if equipment_id:
            return equipment_service.get_equipment(equipment_id)

        dto = make_model_paginated(EquipmentFilterDto, cherrypy.request.params)
        return equipment_service.get_equipments(dto)

    @inject
    def PUT(self, equipment_id: str = None, *, equipment_service: EquipmentServiceDp, **kwargs) -> EquipmentVm:
        cherrypy.request.json["id"] = equipment_id
        dto = make_model(EquipmentUpdateDto, cherrypy.request.json)
        return equipment_service.update_equipment(dto)

    @inject
    def DELETE(self, equipment_id: str = None, *, equipment_service: EquipmentServiceDp, **kwargs):
        equipment_service.delete_equipment(equipment_id)