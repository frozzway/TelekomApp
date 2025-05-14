from typing import TypeVar, Generic, ClassVar

from pydantic import BaseModel, Field, model_validator


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
