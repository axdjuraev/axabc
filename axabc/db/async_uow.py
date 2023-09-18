from abc import ABC, abstractmethod
from typing import Type

from .types import TRepo, TUOW
from .abstract_uow import AbstractUOW
from .base_repo_collector import BaseRepoCollector


class AbstractUOWFactory(ABC):
    def __init__(self, session_maker, repo: Type[BaseRepoCollector]) -> None:
        self.session_maker = session_maker
        self.repo = repo

    @abstractmethod
    def __call__(self) -> AbstractUOW:
        raise NotImplementedError

