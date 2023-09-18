from abc import ABC, abstractmethod
from typing import Type, TypeVar
from .types import TRepo
from .abstract_repo_collector import AbstractRepoCollector


AbstractTRepoCollector = TypeVar("AbstractTRepoCollector", bound=AbstractRepoCollector)


class AbstractUOW(ABC):
    def __init__(self, repo: Type[AbstractRepoCollector], sessions_mapper: dict) -> None:
        self.repo = repo(_uow=self)
        self.sessions_mapper = sessions_mapper

    @abstractmethod
    def get_repo(self, repo_cls: Type[TRepo]) -> TRepo:
        raise NotImplementedError

