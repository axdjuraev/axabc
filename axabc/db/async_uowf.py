from typing import Generic, Optional, Type

from .session_mapper import SessionMaker, SessionMapper, SessionMakersMapper
from .async_uow import AsyncUOW, TRepoCollector
from .abstract_uowf import AbstractUOWFactory 


class AsyncUOWFactory(AbstractUOWFactory, Generic[TRepoCollector]):
    def __init__(self, repo: Type[TRepoCollector], session_maker: SessionMaker, session_makers_mapper: Optional[dict[str, SessionMaker]] = None) -> None:
        session_makers_mapper = session_makers_mapper or {}
        self.repo = repo
        self.session_maker = session_maker
        self.session_makers_mapper = SessionMakersMapper(self.repo, session_maker, session_makers_mapper)

    def __call__(self) -> AsyncUOW[TRepoCollector]:
        return AsyncUOW(self.repo, SessionMapper(self.session_makers_mapper))

