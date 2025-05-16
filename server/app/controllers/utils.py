from typing import Type, TypeVar
from http import HTTPStatus

from cherrypy import HTTPError
from pydantic import BaseModel, ValidationError

from app.models import PaginatedQuery


T = TypeVar('T', bound=BaseModel)


def make_model(model_type: Type[T], data: dict | list) -> T | list[T]:
    if isinstance(data, list):
        return [dict_to_model(model_type, i) for i in data]
    elif isinstance(data, dict):
        return dict_to_model(model_type, data)
    raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY, "Invalid data")


def dict_to_model(model_type: Type[T], data: dict) -> T:
    if not isinstance(data, dict):
        raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY, "Invalid data")

    try:
        return model_type(**data)
    except ValidationError as e:
        raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY, e.json())


def make_model_paginated(model_type: Type[T], params: dict) -> PaginatedQuery[T]:
    model_fields = model_type.model_fields.keys()
    if any(field in params for field in model_fields):
        filters = dict_to_model(model_type, params)
    else:
        filters = None

    pagination_values = {}
    for key in PaginatedQuery.pagination_keys:
        if key in params:
            pagination_values[key] = params[key]

    try:
        return PaginatedQuery[model_type](  # type: ignore
            filter=filters,
            **pagination_values)
    except ValidationError as e:
        raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY, e.json())