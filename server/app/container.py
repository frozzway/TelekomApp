from dependency_injector import containers, providers

from app.database import get_session
from app.services import EquipmentService
from app.services import EquipmentTypeService
from app.services import PrefillService
from app.services import AuthService


class Container(containers.DeclarativeContainer):
    session = providers.Resource(get_session)
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
    auth_service = providers.Factory(
        AuthService,
        session=session,
    )
