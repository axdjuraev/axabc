from abc import ABC, abstractmethod
from dataclasses import dataclass, Field
from typing import Any, Iterable, Type, Union

from axabc.initialization.annotation import get_initializable_annotations
from .async_repository import AbstractAsyncRepository
from .types import TRepo, TUOW
from .abstract_uow import AbstractUOW


@dataclass
class BaseRepoCollector(ABC):
    _uow: Union[AbstractUOW, None] = None
    _repos: dict = Field(default_factory=lambda: {})  # type: ignore

    def __init__(self) -> None:
        self.init_repos()

    def __getattribute__(self, __name: str) -> Any:
        try:
            attr = super().__getattribute__(__name)
            return attr
        except AttributeError:
            repo = self._repos.get(__name)

            if repo is None:
                raise
            if self._uow is None:
                raise NotImplementedError

            return self._uow.get_repo(repo)

    def init_repos(self):
        self._repos = {}

        for name_, type_ in get_initializable_annotations(self.__class__, AbstractAsyncRepository):
            self._repos[name_] = type_

    def get_repos(self) -> Iterable:
        return self._repos.keys()


class AbstractUOWFactory(ABC):
    def __init__(self, session_maker, repo: Type[BaseRepoCollector]) -> None:
        self.session_maker = session_maker
        self.repo = repo

    @abstractmethod
    def __call__(self) -> AbstractUOW:
        raise NotImplementedError
