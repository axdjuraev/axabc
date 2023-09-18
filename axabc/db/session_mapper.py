from typing import Protocol, runtime_checkable
from .repo_collector import BaseRepoCollector


@runtime_checkable
class Session(Protocol):
    async def begin(self):
        raise NotImplementedError

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
    
    async def close(self):
        raise NotImplementedError


@runtime_checkable
class SessionMaker(Protocol):
    def __call__(self, *args, **kwargs) -> Session:
        raise NotImplementedError


class SessionMakersMapper:
    def __init__(self, repos: BaseRepoCollector, common: SessionMaker, mapper: dict[str, SessionMaker]) -> None:
        self.repos = repos
        self.common = common
        self.mapper = mapper
        self._verify_session_makers()

    def _verify_session_makers(self):
        for repo_name in self.repos.get_repos():
            session_maker = self.get(repo_name)

            if not session_maker:
                raise NotImplementedError(f'`{repo_name}`.session_maker not found')

            if not isinstance(session_maker, SessionMaker):
                raise NotImplementedError(f'`{repo_name}`.session_maker is not instance of SessionMaker')

    def get(self, repo_name: str) -> SessionMaker:
        return self.mapper.get(repo_name) or self.common


class SessionMapper:
    def __init__(self, session_makers_mapper: SessionMakersMapper) -> None:
        self.session_makers_mapper = session_makers_mapper
        self.used_sessions: dict[SessionMaker, Session] = {}

    def get_session(self, repo_name: str) -> Session:
        maker = self.session_makers_mapper.get(repo_name)
        if maker in self.used_sessions:
            return self.used_sessions[maker] 
        
        session = maker()
        self.used_sessions[maker] = session
        return session   

    async def require(self, repo_name: str) -> Session:
        session = self.get_session(repo_name)
        await session.begin()
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

