from typing import TypeVar
from pydantic import BaseModel


__all__ = [
    'TIModel',
    'TOModel',
]


TIModel = TypeVar("TIModel", bound=BaseModel)
TOModel = TypeVar("TOModel", bound=BaseModel)

