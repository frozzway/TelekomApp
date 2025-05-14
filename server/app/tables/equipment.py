import re

from sqlalchemy import ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.tables import EntityWithId


class Equipment(EntityWithId):
    """Оборудование"""

    __tablename__ = "Equipment"

    note: Mapped[str] = mapped_column(String(1000), default='')
    equipment_type_id: Mapped[int] = mapped_column(ForeignKey('EquipmentType.id'))
    serial_number: Mapped[str] = mapped_column(String(100))
    is_deleted: Mapped[bool] = mapped_column(default=False)

    uq_name = 'uq_serial_per_type'
    __table_args__ = (
        UniqueConstraint('serial_number', 'equipment_type_id', name=uq_name),
    )


class EquipmentType(EntityWithId):
    """Тип оборудования"""

    __tablename__ = "EquipmentType"

    name: Mapped[str] = mapped_column(String(1000))
    serial_number_mask: Mapped[str] = mapped_column(String(100))

    def regex_mask(self):
        mask_map = {
            'N': '\\d',
            'A': '[A-Z]',
            'a': '[a-z]',
            'X': '[A-Z0-9]',
            'Z': '[-_@]',
        }

        pattern = ''.join(mask_map.get(c, re.escape(c)) for c in self.serial_number_mask)
        return re.compile(f'^{pattern}$')
