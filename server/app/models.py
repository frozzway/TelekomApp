from typing import Annotated, Generic, TypeVar, ClassVar

from pydantic import BaseModel, AfterValidator, Field, ConfigDict
from pydantic import model_validator


def correct_mask(value: str):
    allowed_chars = {'N', 'A', 'a', 'X', 'Z'}
    if not all(c in allowed_chars for c in value):
        raise ValueError(f"Маска может содержать только {', '.join(allowed_chars)}")
    return value


EquipmentMask = Annotated[str, AfterValidator(correct_mask)]


class EquipmentUpdateDto(BaseModel):
    id: int
    note: str
    equipment_type_id: int
    serial_number: str


class EquipmentVm(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    note: str
    equipment_type_id: int
    serial_number: str


class EquipmentGridVm(EquipmentVm):
    equipment_type_name: str


class EquipmentFilterDto(BaseModel):
    note: str | None = Field(None)
    equipment_type_id: int | None = Field(None)
    serial_number: str | None = Field(None)


class EquipmentTypeVm(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    serial_number_mask: EquipmentMask


class EquipmentTypeFilterDto(BaseModel):
    name: str | None = Field(None)
    serial_number_mask: EquipmentMask | None = Field(None)


class EquipmentTypePrefillDto(BaseModel):
    name: str
    serial_number_mask: EquipmentMask


class EquipmentCreateDto(BaseModel):
    note: str
    equipment_type_id: int
    serial_numbers: list[str]


class EquipmentCreateResult(BaseModel):
    success_list: list[EquipmentVm]
    invalid_serial_numbers: list[str]


TFilter = TypeVar('TFilter')


class PaginatedQuery(BaseModel, Generic[TFilter]):
    skip: int | None = Field(None, ge=0)
    take: int | None = Field(None, ge=1)
    require_total_count: bool = Field(False)
    filter: TFilter | None = Field(None)

    pagination_keys: ClassVar = ("skip", "take", "require_total_count")

    @model_validator(mode="after")
    def _check_skip_take(self) -> "PaginatedQuery[TFilter]":
        if (self.skip is None) ^ (self.take is None):
            raise ValueError("Поля `skip` и `take` должны указываться вместе")
        return self


TResult = TypeVar('TResult')


class PaginatedQueryResult(BaseModel, Generic[TResult]):
    data: list[TResult]
    total_count: int