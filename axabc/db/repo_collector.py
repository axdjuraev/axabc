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

    def __init_subclass__(cls) -> None:
        if cls.__abstract__ and '__abstract__' in cls.__dict__:
            return print(f'axlog: cancel from {cls.__name__}')

        cls.init_repos()

        for parent in cls.mro():
            if not issubclass(parent, BaseRepoCollector) or parent.__abstract__:
                break
            print(f'axlog: inherit from {parent.__name__}')
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
            print(f'axlog init repo: {name_}')
            cls._repos[name_] = type_
    
    @classmethod
    def get_repos(cls) -> Iterable:
        if cls._repos is None:
            raise

        return cls._repos.keys()

