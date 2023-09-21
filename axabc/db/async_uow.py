from typing import Generic, Type, TypeVar

from .abstract_uow import AbstractUOW
from .async_repository import AbstractAsyncRepository
from .repo_collector import BaseRepoCollector
from .session_mapper import SessionMapper
from .combined_repository import CombinedRepository


TRepoCollector = TypeVar('TRepoCollector', bound=BaseRepoCollector)


class AsyncUOW(AbstractUOW, Generic[TRepoCollector]):
    def __init__(self, repo: Type[TRepoCollector], sessions_mapper: SessionMapper) -> None:
        self.repo: TRepoCollector = repo()
        self.repo._uow = self
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

    def get_repo(self, repo_cls: Type[AbstractAsyncRepository]) -> AbstractAsyncRepository:
        if self.is_session_closed:
            raise ValueError("use uow in context manager")
        
        repo_name = repo_cls.__name__ 
        if not repo_name in self.used_repos:
            session = self if issubclass(repo_cls, CombinedRepository) else self.sessions_mapper.require(repo_name)
            self.used_repos[repo_name] = repo_cls(session)

        return self.used_repos[repo_name]

