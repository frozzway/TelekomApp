from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field


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
