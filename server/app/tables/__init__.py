from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True


class EntityWithId(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class EntityWithUUID(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


from .equipment import Equipment, EquipmentType
