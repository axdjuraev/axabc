import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Type, TypeVar, Union

from db.async_repository import AbstractAsyncRepository

TRepo = TypeVar("TRepo", bound=AbstractAsyncRepository)


class AbstractAsyncUOW(ABC):
    @abstractmethod
    def get_repo(self, repo_cls: Type[TRepo]) -> TRepo:
        raise NotImplementedError


@dataclass
class BaseRepoCollector(ABC):
    _uow: Union[AbstractAsyncUOW, None] = None

    def __getattribute__(self, __name: str) -> Any:
        attr = super().__getattribute__(__name)

        if inspect.isclass(attr) and issubclass(attr, AbstractAsyncRepository):
            if self._uow is None:
                raise NotImplementedError("uow of the collection is not known")

            return self._uow.get_repo(attr)

        return attr
