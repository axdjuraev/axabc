from typing import Protocol, Type, runtime_checkable
from .repo_collector import BaseRepoCollector


@runtime_checkable
class LazySession(Protocol):
    is_begun: bool = False

    async def execute(self):
        if not self.is_begun:
            self.is_begun = True
            # start session
        raise NotImplementedError
        
    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
    
    async def close(self):
        raise NotImplementedError


@runtime_checkable
class LazySessionMaker(Protocol):
    def __call__(self, *args, **kwargs) -> LazySession:
        raise NotImplementedError


class SessionMakersMapper:
    def __init__(self, repos: Type[BaseRepoCollector], common: LazySessionMaker, mapper: dict[str, LazySessionMaker]) -> None:
        self.repos = repos
        self.common = common
        self.mapper = mapper
        self._verify_session_makers()

    def _verify_session_makers(self):
        for repo_name in self.repos.get_repos():
            session_maker = self.get(repo_name)

            if not session_maker:
                raise NotImplementedError(f'`{repo_name}`.session_maker not found')

            if not isinstance(session_maker, LazySessionMaker):
                raise NotImplementedError(f'`{repo_name}`.session_maker is not instance of LazySessionMaker')

    def get(self, repo_name: str) -> LazySessionMaker:
        return self.mapper.get(repo_name) or self.common


class SessionMapper:
    def __init__(self, session_makers_mapper: SessionMakersMapper) -> None:
        self.session_makers_mapper = session_makers_mapper
        self.used_sessions: dict[LazySessionMaker, LazySession] = {}

    def get_session(self, repo_name: str) -> LazySession:
        maker = self.session_makers_mapper.get(repo_name)
        if maker in self.used_sessions:
            return self.used_sessions[maker] 
        
        session = maker()
        self.used_sessions[maker] = session
        return session   

    def require(self, repo_name: str) -> LazySession:
        session = self.get_session(repo_name)
        return session

    async def commit(self):
        for session in self.used_sessions.values():
            await session.commit()

    async def rollback(self):
        for session in self.used_sessions.values():
            await session.rollback()
    
    async def close(self):
        for session in self.used_sessions.values():
            await session.close()

