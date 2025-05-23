from datetime import datetime

from sqlalchemy import ForeignKey, Table, Column, TIMESTAMP, String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from app.tables import EntityWithUUID, EntityWithId, Base


user_role_table = Table(
    "UserRoles",
    Base.metadata,
    Column("UserId", ForeignKey("Users.id")),
    Column("RoleId", ForeignKey("Roles.id")),
)


class User(EntityWithUUID):
    """Пользователь"""

    __tablename__ = 'Users'

    name: Mapped[str] = mapped_column(String(256))
    middle_name: Mapped[str] = mapped_column(String(256))
    surname: Mapped[str] = mapped_column(String(256))
    hashed_password: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(256))

    is_deleted: Mapped[bool] = mapped_column(default=False)

    roles: Mapped[list['Role']] = relationship(secondary=user_role_table, lazy='selectin')


class RefreshSession(EntityWithId):
    """Сессия для обновления JWT"""

    __tablename__ = 'RefreshSessions'

    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    token_hash: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    expires_in: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    ip_address: Mapped[str] = mapped_column(String(256))
    user_agent: Mapped[str] = mapped_column(String(256))


class Role(EntityWithUUID):
    """Роль пользователя в системе"""

    __tablename__ = 'Roles'
    name: Mapped[str] = mapped_column(String(256), unique=True)
