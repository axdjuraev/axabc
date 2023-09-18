from abc import ABC, abstractmethod
from typing import Generic, Optional, Type

from .types import TRepoCollector
from .uow import AbstractUOW, UOW
from .repo_collector import BaseRepoCollector
from .session_mapper import SessionMaker, SessionMapper, SessionMakersMapper


class AbstractUOWFactory(ABC):
    def __init__(self, session_maker, repo: Type[BaseRepoCollector]) -> None:
        self.session_maker = session_maker
        self.repo = repo

    @abstractmethod
    def __call__(self) -> AbstractUOW:
        raise NotImplementedError


class UOWFactory(AbstractUOWFactory, Generic[TRepoCollector]):
    def __init__(self, repo: Type[TRepoCollector], session_maker: SessionMaker, session_makers_mapper: Optional[dict[str, SessionMaker]] = None) -> None:
        session_makers_mapper = session_makers_mapper or {}
        self.repo = repo
        self.session_maker = session_maker
        self.session_makers_mapper = SessionMakersMapper(self.repo, session_maker, session_makers_mapper)

    def __call__(self) -> UOW[TRepoCollector]:
        return UOW(self.repo, SessionMapper(self.session_makers_mapper))

