from abc import ABC, abstractmethod
from typing import Any, List, Union

from pydantic import BaseModel


class AbstractAsyncRepository(ABC):
    IModel = BaseModel
    OModel = BaseModel

    def __init__(self, session: Any) -> None:
        self.session = session

    @abstractmethod
    async def add(self, obj: IModel) -> Union[IModel, None]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, *identifiers: List[Any]) -> Union[IModel, None]:
        raise NotImplementedError

    async def update(self, obj: IModel) -> Union[IModel, None]:
        raise NotImplementedError

    async def delete(self, obj: IModel) -> None:
        raise NotImplementedError

    async def all(self, *identifier: List[Any]) -> Union[List[OModel], None]:
        raise NotImplementedError
