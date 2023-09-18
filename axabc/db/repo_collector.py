from abc import ABC
from dataclasses import dataclass
from typing import Iterable, Optional

from axabc.initialization.annotation import get_initializable_annotations
from .async_repository import AbstractAsyncRepository
from .abstract_uow import AbstractUOW
from .abstract_repo_collector import AbstractRepoCollector


@dataclass
class BaseRepoCollector(AbstractRepoCollector, ABC):
    __abstract__ = False

    _repos: Optional[dict] = None
    _uow: Optional[AbstractUOW] = None

    def __init_subclass__(cls) -> None:
        if cls.__abstract__ or cls is BaseRepoCollector:
            return
        cls.init_repos()

    def __getattribute__(self, __name: str):
        try:
            attr = super().__getattribute__(__name)
            return attr
        except AttributeError:
            if self.__class__._repos is None:
                raise

            repo = self.__class__._repos.get(__name)

            if repo is None:
                raise

            if self._uow is None:
                raise NotImplementedError

            setattr(self, __name, self._uow.get_repo(repo))
            return getattr(self, __name)

    @classmethod
    def init_repos(cls):
        cls._repos = {}

        for name_, type_ in get_initializable_annotations(cls, AbstractAsyncRepository):
            cls._repos[name_] = type_
    
    @classmethod
    def get_repos(cls) -> Iterable:
        if cls._repos is None:
            raise

        return cls._repos.keys()

