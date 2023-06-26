from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Union

from pydantic import BaseModel

TModel = TypeVar('TModel')

class AbstractAsyncRepository(ABC):
    Model = BaseModel
    OModel = BaseModel

    def __init__(self, session: Any) -> None:
        self.session = session

    @abstractmethod
    async def add(self, obj: Model) -> Union[Model, None]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, *identifiers: List[Any]) -> Union[Model, None]:
        raise NotImplementedError

    async def update(self, obj: Model) -> Union[Model, None]:
        raise NotImplementedError

    async def delete(self, obj: Model) -> None:
        raise NotImplementedError

    async def all(self, *identifier: List[Any]) -> Union[List[OModel], None]:
        raise NotImplementedError
