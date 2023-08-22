from abc import ABC, abstractmethod
from typing import Any, List


class AbstractAsyncRepository(ABC):
    def __init__(self, session: Any) -> None:
        self.session = session

    @abstractmethod
    async def add(self, obj):
        raise NotImplementedError

    @abstractmethod
    async def get(self, *identifiers: List[Any]):
        raise NotImplementedError

    async def update(self, obj):
        raise NotImplementedError

    async def delete(self, obj) -> None:
        raise NotImplementedError

    async def all(self, *identifier: List[Any]):
        raise NotImplementedError
