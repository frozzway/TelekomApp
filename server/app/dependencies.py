from typing import Annotated

from dependency_injector.wiring import Provide

from app.services import EquipmentService, AuthService
from app.container import Container
from app.services import EquipmentTypeService


EquipmentServiceDp = Annotated[EquipmentService, Provide[Container.equipment_service]]
EquipmentTypeServiceDp = Annotated[EquipmentTypeService, Provide[Container.equipment_type_service]]
AuthServiceDp = Annotated[AuthService, Provide[Container.auth_service]]
