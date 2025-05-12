import re

from cherrypy import HTTPError
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.services import EquipmentTypeService
from app.tables import EquipmentType, Equipment
from app.models import PaginatedQuery, PaginatedQueryResult
from app.models import (EquipmentCreateDto, EquipmentCreateResult, EquipmentVm, EquipmentGridVm,
                        EquipmentFilterDto, EquipmentUpdateDto)


class EquipmentService:
    """Сервис для работы с сущностью 'Оборудование'"""

    conflict_message = "Оборудование с таким серийным номером уже существует для этого типа"

    def __init__(self, session: Session, equipment_type_service: EquipmentTypeService):
        self.session = session
        self.equipment_type_service = equipment_type_service

    def create_equipments(self, dto: EquipmentCreateDto) -> EquipmentCreateResult:
        """
        Метод создания сущности 'Оборудование'

        Arguments:
            dto: объект передачи данных для сущности 'Оборудование'

        Returns:
            Модель отображения результата операции создания сущности 'Оборудование'
        """

        equipment_type = self.equipment_type_service.get_equipment_type(dto.equipment_type_id)
        mask_pattern = equipment_type.regex_mask()

        invalid_serial_numbers = []
        entities = []
        for serial_number in dto.serial_numbers:
            if not re.match(mask_pattern, serial_number):
                invalid_serial_numbers.append(serial_number)
                continue
            entity = Equipment(
                note=dto.note,
                serial_number=serial_number,
                equipment_type_id=dto.equipment_type_id)
            entities.append(entity)

        self.session.add_all(entities)

        try:
            self.session.flush()
            result = EquipmentCreateResult(
                success_list=[EquipmentVm.model_validate(entity) for entity in entities],
                invalid_serial_numbers=invalid_serial_numbers)
            self.session.commit()
        except IntegrityError as e:
            if Equipment.uq_name in str(e.orig):
                raise HTTPError(409, EquipmentService.conflict_message)
            raise e
        return result

    def update_equipment(self, dto: EquipmentUpdateDto) -> EquipmentVm:
        """
        Метод редактирования сущности 'Оборудование'

        Arguments:
            dto: объект передачи данных для сущности 'Оборудование'

        Returns:
            Модель отображения сущности 'Оборудование'
        """

        entity = self._get_equipment(dto.id)
        dumped_model = dto.model_dump()
        for field in dumped_model.keys():
            new_value = dumped_model.get(field)
            setattr(entity, field, new_value)
        try:
            self.session.commit()
        except IntegrityError as e:
            if Equipment.uq_name in str(e.orig):
                raise HTTPError(409, EquipmentService.conflict_message)
        return EquipmentVm.model_validate(entity)

    def delete_equipment(self, equipment_id) -> None:
        """
        Метод удаления сущности 'Оборудование'

        Arguments:
            equipment_id: идентификатор сущности 'Оборудование'
        """

        entity = self._get_equipment(equipment_id)
        entity.is_deleted = True
        self.session.commit()

    def _get_equipment(self, equipment_id: int) -> Equipment:
        """
        Метод получения сущности 'Оборудование'

        Arguments:
            equipment_id: идентификатор сущности 'Оборудование'

        Returns:
            Сущность 'Оборудование'
        """

        equipment = self.session.query(Equipment) \
            .where((Equipment.id == equipment_id) & (Equipment.is_deleted.is_(False))) \
            .scalar()
        if equipment is None:
            raise HTTPError(status=404)
        return equipment

    def get_equipments(self, query: PaginatedQuery[EquipmentFilterDto]) -> PaginatedQueryResult[EquipmentGridVm]:
        """
        Метод получения табличных данных сущности 'Оборудование'

        Arguments:
            query: объект передачи данных с фильтрами и параметрами пагинации

        Returns:
            Данные для подстановки в таблицу
        """

        filters = query.filter.model_dump(exclude_unset=True) if query.filter else {}
        filters['is_deleted'] = False

        total_count = -1
        if query.require_total_count:
            count_stmt = select(func.count()).select_from(Equipment).filter_by(**filters)
            total_count = self.session.execute(count_stmt).scalar_one()

        conditions = [
            getattr(Equipment, key) == value
            for key, value in filters.items()
        ]

        stmt = select(Equipment, EquipmentType.name) \
            .join(EquipmentType, Equipment.equipment_type_id == EquipmentType.id) \
            .filter(*conditions) \
            .order_by(Equipment.id)

        if query.skip is not None:
            stmt = stmt.offset(query.skip).limit(query.take)

        rows = self.session.execute(stmt).all()

        return PaginatedQueryResult[EquipmentGridVm](
            data=[EquipmentGridVm.model_validate({**eq.__dict__, 'equipment_type_name': name}) for eq, name in rows],
            total_count=total_count)

    def get_equipment(self, equipment_id) -> EquipmentVm:
        """
        Метод получения сущности 'Оборудование'

        Arguments:
            equipment_id: идентификатор сущности 'Оборудование'

        Returns:
            Модель отображения сущности 'Оборудование'
        """

        equipment = self._get_equipment(equipment_id)
        vm = EquipmentVm.model_validate(equipment)
        return vm
