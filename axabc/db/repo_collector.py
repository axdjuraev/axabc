from abc import ABC
from dataclasses import field, dataclass
from typing import Iterable

from axabc.initialization.annotation import get_initializable_annotations
from .async_repository import AbstractAsyncRepository
from .abstract_uow import AbstractUOW


@dataclass
class BaseRepoCollector(ABC):
    _uow: AbstractUOW
    _repos: dict = field(default_factory=lambda: {})

    def __init__(self) -> None:
        self.init_repos()

    def __getattribute__(self, __name: str):
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

