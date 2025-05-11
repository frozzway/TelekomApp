from typing import Annotated

from dependency_injector.wiring import Provide

from app.services import EquipmentService
from app.container import Container
from app.services import EquipmentTypeService


EquipmentServiceDp = Annotated[EquipmentService, Provide[Container.equipment_service]]
EquipmentTypeServiceDp = Annotated[EquipmentTypeService, Provide[Container.equipment_type_service]]