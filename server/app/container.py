from dependency_injector import containers, providers

from app.database import session_maker
from app.services import EquipmentService
from app.services import EquipmentTypeService
from app.services import PrefillService


class Container(containers.DeclarativeContainer):
    session = providers.Factory(session_maker)
    equipment_type_service = providers.Factory(
        EquipmentTypeService,
        session=session,
    )
    equipment_service = providers.Factory(
        EquipmentService,
        session=session,
        equipment_type_service=equipment_type_service,
    )
    prefill_service = providers.Factory(
        PrefillService,
        session=session,
    )