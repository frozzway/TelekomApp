from typing import Annotated

from dependency_injector.wiring import Provide, Closing

from app.services import EquipmentService, AuthService
from app.container import Container
from app.services import EquipmentTypeService


EquipmentServiceDp = Annotated[EquipmentService, Closing[Provide[Container.equipment_service]]]
EquipmentTypeServiceDp = Annotated[EquipmentTypeService, Closing[Provide[Container.equipment_type_service]]]
AuthServiceDp = Annotated[AuthService, Closing[Provide[Container.auth_service]]]
