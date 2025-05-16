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
        """
        Метод создания сущности 'Оборудование'
        :param equipment_service: Сервис для работы с сущностью 'Оборудование'
        :return: Модель отображения результата операции создания сущности
        """

        dto = make_model(EquipmentCreateDto, cherrypy.request.json)
        return equipment_service.create_equipments(dto)

    @inject
    def GET(self, equipment_id: str = None, *, equipment_service: EquipmentServiceDp, **kwargs
            ) -> PaginatedQueryResult[EquipmentGridVm] | EquipmentVm:
        """
        Метод получения сущности 'Оборудование' или табличных данных сущности 'Оборудование'
        :param equipment_id: идентификатор сущности
        :param equipment_service: Сервис для работы с сущностью 'Оборудование'
        :return: Модель отображения сущности / Данные для подстановки в таблицу
        """

        if equipment_id:
            return equipment_service.get_equipment(equipment_id)

        dto = make_model_paginated(EquipmentFilterDto, cherrypy.request.params)
        return equipment_service.get_equipments(dto)

    @inject
    def PUT(self, equipment_id: str = None, *, equipment_service: EquipmentServiceDp, **kwargs) -> EquipmentVm:
        """
        Метод редактирования сущности 'Оборудование'
        :param equipment_id: идентификатор сущности
        :param equipment_service: Сервис для работы с сущностью 'Оборудование'
        :return: Модель отображения сущности
        """

        cherrypy.request.json["id"] = equipment_id
        dto = make_model(EquipmentUpdateDto, cherrypy.request.json)
        return equipment_service.update_equipment(dto)

    @inject
    def DELETE(self, equipment_id: str = None, *, equipment_service: EquipmentServiceDp, **kwargs) -> None:
        """
        Метод удаления сущности 'Оборудование'
        :param equipment_id: идентификатор сущности
        :param equipment_service: Сервис для работы с сущностью 'Оборудование'
        """

        equipment_service.delete_equipment(equipment_id)