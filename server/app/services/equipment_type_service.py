from cherrypy import HTTPError
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import EquipmentTypeFilterDto
from app.models import EquipmentTypeVm
from app.models import PaginatedQuery
from app.models import PaginatedQueryResult
from app.tables import EquipmentType


class EquipmentTypeService:
    """Сервис для работы с сущностью 'Тип оборудования'"""

    def __init__(self, session: Session):
        self.session = session

    def get_entities(self, query: PaginatedQuery[EquipmentTypeFilterDto]) -> PaginatedQueryResult[EquipmentTypeVm]:
        """
        Метод получения табличных данных сущности

        Arguments:
            query: объект передачи данных с фильтрами и параметрами пагинации

        Returns:
            Данные для подстановки в таблицу
        """

        filters = query.filter.model_dump(exclude_unset=True) if query.filter else {}

        total_count = -1
        if query.require_total_count:
            count_stmt = select(func.count()).select_from(EquipmentType).filter_by(**filters)
            total_count = self.session.execute(count_stmt).scalar_one()

        stmt = select(EquipmentType).filter_by(**filters).order_by(EquipmentType.id)
        if query.skip is not None:
            stmt = stmt.offset(query.skip).limit(query.take)

        entities = self.session.execute(stmt).scalars().all()
        return PaginatedQueryResult[EquipmentTypeVm](
            data=[EquipmentTypeVm.model_validate(entity) for entity in entities],
            total_count=total_count)

    def get_equipment_type(self, equipment_type_id: int) -> EquipmentType:
        """
        Метод получения сущности

        Arguments:
            equipment_type_id: идентификатор сущности

        Returns:
            Сущность 'Тип оборудования'
        """

        equipment_type = self.session.query(EquipmentType) \
            .where(EquipmentType.id == equipment_type_id) \
            .scalar()
        if equipment_type is None:
            raise HTTPError(status=404)
        return equipment_type
