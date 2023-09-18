from typing import Type
from abc import ABC, abstractmethod
from .abstract_uow import AbstractUOW, AbstractTRepoCollector


class AbstractUOWFactory(ABC):
    def __init__(self, session_maker, repo: Type[AbstractTRepoCollector]) -> None:
        self.session_maker = session_maker
        self.repo = repo

    @abstractmethod
    def __call__(self) -> AbstractUOW:
        raise NotImplementedError

