from typing import TypeVar
from pydantic import BaseModel
from .async_repository import AbstractAsyncRepository


__all__ = [
    'TIModel',
    'TOModel',
]


TIModel = TypeVar("TIModel", bound=BaseModel)
TOModel = TypeVar("TOModel", bound=BaseModel)
TRepo = TypeVar("TRepo", bound=AbstractAsyncRepository)
TUOW = TypeVar("TUOW", bound=AbstractAsyncRepository)

