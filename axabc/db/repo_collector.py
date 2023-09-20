from abc import ABC
from typing import Iterable, Optional

from axabc.initialization.annotation import get_initializable_annotations
from .async_repository import AbstractAsyncRepository
from .abstract_uow import AbstractUOW
from .abstract_repo_collector import AbstractRepoCollector


class BaseRepoCollector(AbstractRepoCollector, ABC):
    __abstract__ = True

    _repos: Optional[dict] = None
    _uow: Optional[AbstractUOW] = None


    @staticmethod
    def _is_abstract(cls_):
        return cls_.__abstract__ and '__abstract__' in cls_.__dict__

    def __init_subclass__(cls) -> None:
        if cls._is_abstract(cls):
            return 

        cls.init_repos()

        for parent in cls.mro():
            if not issubclass(parent, BaseRepoCollector) or cls._is_abstract(parent):
                break
            cls._repos.update(parent._repos)  # type: ignore

    def __getattribute__(self, __name: str):
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            if self.__class__._repos is None:
                raise NotImplementedError

            repo = self.__class__._repos.get(__name)

            if repo is None:
                raise ValueError

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
            cls.init_repos()

        return cls._repos.keys()  # type: ignore

