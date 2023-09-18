from typing import TypeVar
from pydantic import BaseModel
from .async_repository import AbstractAsyncRepository
from .repo_collector import BaseRepoCollector


__all__ = [
    'TIModel',
    'TOModel',
]


TIModel = TypeVar("TIModel", bound=BaseModel)
TOModel = TypeVar("TOModel", bound=BaseModel)
TRepo = TypeVar("TRepo", bound=AbstractAsyncRepository)
TRepoCollector = TypeVar("TRepoCollector", bound=BaseRepoCollector)

