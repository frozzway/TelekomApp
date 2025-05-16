import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import EquipmentTypePrefillDto
from app.services import AuthService
from app.tables import EquipmentType, Equipment, User, Role
from app.roles import Role as RoleEnum


class PrefillService:
    """Класс для предзаполнения базы данных"""

    equipment_type_path = Path.cwd() / "resources" / "equipment_types.json"

    def __init__(self, session: Session):
        self.session = session

    def prefill_equipment_types(self):
        """Метод предзаполнения сущности 'Тип оборудования'"""

        if self.session.query(EquipmentType).count() > 0:
            return
        with open(self.equipment_type_path) as f:
            data = json.load(f)
        dtos = [EquipmentTypePrefillDto(**item) for item in data]
        entities = [EquipmentType(**dto.model_dump()) for dto in dtos]
        self.session.add_all(entities)
        self.session.commit()

    def prefill_equipments(self):
        """Метод предзаполнения сущности 'Оборудование'"""

        if self.session.query(Equipment).count() > 0:
            return
        equipment_type = self.session.query(EquipmentType).where(EquipmentType.name == 'Test Type').first()
        if not equipment_type:
            return
        for i in range(100):
            self.session.add(
                Equipment(
                    equipment_type_id=equipment_type.id,  # type: ignore
                    serial_number=f'{i:04}'))
        self.session.commit()

    def prefill_users(self):
        """Метод предзаполнения пользователей"""

        self._create_admin_account()

    def _create_admin_account(self):
        """Создать аккаунт под администратора"""

        password_hash = AuthService.hash_string('qwerty123!')
        root_role = self.session.query(Role).where(Role.name == RoleEnum.Root.value).scalar()
        admin = self.session.query(User).where(User.email == 'administrator@localhost.ru').scalar()
        if admin:
            return
        admin = User(
            name='Admin',
            middle_name='Admin',
            surname='Admin',
            email='administrator@localhost.ru',
            hashed_password=password_hash,
            roles=[root_role])
        self.session.add(admin)
        self.session.commit()

    def create_roles(self):
        """Записать роли в базу данных"""

        role_names = self.session.scalars(select(Role.name))
        for role in RoleEnum:
            if role.value not in role_names:
                entity = Role(name=role.value)
                self.session.add(entity)
        self.session.commit()
