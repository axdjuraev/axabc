from abc import ABC, abstractmethod
from typing import Generic, Type, Any

from .async_repository import AbstractAsyncRepository
from .types import TRepo, TRepoCollector


class AbstractUOW(ABC):
    def __init__(self, repo, sessions_mapper: dict) -> None:
        self.repo = repo(_uow=self)
        self.sessions_mapper = sessions_mapper

    @abstractmethod
    def get_repo(self, repo_cls: Type[TRepo]) -> TRepo:
        raise NotImplementedError


class UOW(AbstractUOW, Generic[TRepoCollector]):
    def __init__(self, repo: Type[TRepoCollector], sessions_mapper: dict) -> None:
        self.repo: TRepoCollector = repo(_uow=self)  # type: ignore
        self.sessions_mapper = sessions_mapper
        self.is_session_closed: bool = False

    async def __aenter__(self):
        await self.session.begin()
        return self

    async def __aexit__(self, *args, **kwargs):
        if any(args) or kwargs:
            await self.session.rollback()
        else:
            await self.session.commit()

        await self.dispose()

    async def save(self):
        await self.session.commit()

    async def dispose(self):
        await self.session.close()
        self.is_session_closed = True

    async def rollback(self):
        await self.session.rollback()

    def get_repo(self, cls: Type[AbstractAsyncRepository]) -> AbstractAsyncRepository:
        if self.is_session_closed:
            raise ValueError("use uow in context manager")

        return cls(self.sessions_mapper)

