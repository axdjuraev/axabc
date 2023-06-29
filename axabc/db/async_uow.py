import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Type, TypeVar, Union

from .async_repository import AbstractAsyncRepository

TRepo = TypeVar("TRepo", bound=AbstractAsyncRepository)


TUOW = TypeVar("TUOW", bound=AbstractAsyncRepository)


class AbstractUOW(ABC):
    def __init__(self, repo, session: Any) -> None:
        self.repo = repo(_uow=self)
        self.session = session

    @abstractmethod
    def get_repo(self, repo_cls: Type[TRepo]) -> TRepo:
        raise NotImplementedError


@dataclass
class BaseRepoCollector(ABC):
    _uow: Union[AbstractUOW, None] = None
    _repos = None

    def __getattribute__(self, __name: str) -> Any:
        try:
            attr = super().__getattribute__(__name)
            return attr
        except AttributeError:
            if self._repos is None:
                self.init_repos()

            if self._repos is not None:
                repo = self._repos.get(__name)

                if repo is None:
                    raise
                if self._uow is None:
                    raise NotImplementedError

                return self._uow.get_repo(repo)

            raise

    def init_repos(self):
        self._repos = {}

        for name_, type_ in self.__class__.__annotations__.items():
            if not inspect.isclass(type_):
                raise NotImplementedError

            if issubclass(type_, AbstractAsyncRepository):
                self._repos[name_] = type_


class AbstractUOWFactory(ABC):
    def __init__(self, session_maker, repo: Type[BaseRepoCollector]) -> None:
        self.session_maker = session_maker
        self.repo = repo

    @abstractmethod
    def __call__(self) -> AbstractUOW:
        raise NotImplementedError
