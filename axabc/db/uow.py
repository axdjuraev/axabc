from abc import ABC, abstractmethod
from typing import Generic, Type

from .async_repository import AbstractAsyncRepository
from .types import TRepo, TRepoCollector
from .session_mapper import SessionMapper


class AbstractUOW(ABC):
    def __init__(self, repo, sessions_mapper: dict) -> None:
        self.repo = repo(_uow=self)
        self.sessions_mapper = sessions_mapper

    @abstractmethod
    def get_repo(self, repo_cls: Type[TRepo]) -> TRepo:
        raise NotImplementedError


class UOW(AbstractUOW, Generic[TRepoCollector]):
    def __init__(self, repo: Type[TRepoCollector], sessions_mapper: SessionMapper) -> None:
        self.repo: TRepoCollector = repo(_uow=self)  # type: ignore
        self.sessions_mapper = sessions_mapper
        self.is_session_closed: bool = False
        self.used_repos: dict[str, AbstractAsyncRepository] = {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        if any(args) or kwargs:
            await self.dispose()
        else:
            await self.save()

        await self.dispose()

    async def save(self):
        await self.sessions_mapper.commit()

    async def dispose(self):
        await self.sessions_mapper.close()
        self.is_session_closed = True

    def get_repo(self, cls: Type[AbstractAsyncRepository]) -> AbstractAsyncRepository:
        if self.is_session_closed:
            raise ValueError("use uow in context manager")
        
        repo_name = cls.__name__ 
        if not repo_name in self.used_repos:
            session = self.sessions_mapper.require(repo_name)
            self.used_repos[repo_name] = cls(session)

        return self.used_repos[repo_name]

