from abc import ABC
from dataclasses import dataclass
from typing import Iterable, Optional

from axabc.initialization.annotation import get_initializable_annotations
from .async_repository import AbstractAsyncRepository
from .abstract_uow import AbstractUOW
from .abstract_repo_collector import AbstractRepoCollector


@dataclass
class BaseRepoCollector(AbstractRepoCollector, ABC):
    _uow: Optional[AbstractUOW] = None
    _repos: Optional[dict] = None

    def __getattribute__(self, __name: str):
        try:
            attr = super().__getattribute__(__name)
            return attr
        except AttributeError:
            if self._repos is None:
                self.init_repos()

            repo = self._repos.get(__name)  # type: ignore
            if repo is None:
                raise
            if self._uow is None:
                raise NotImplementedError

            return self._uow.get_repo(repo)

    @classmethod
    def init_repos(cls):
        cls._repos = {}

        for name_, type_ in get_initializable_annotations(cls, AbstractAsyncRepository):
            cls._repos[name_] = type_
    
    @classmethod
    def get_repos(cls) -> Iterable:
        if cls._repos is None:
            cls.init_repos()

        return cls._repos.keys()  # type: ignore

