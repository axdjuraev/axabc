from abc import ABC, abstractmethod
from typing import Type, Any
from .types import TRepo


class AbstractUOW(ABC):
    def __init__(self, repo, session: Any) -> None:
        self.repo = repo(_uow=self)
        self.session = session

    @abstractmethod
    def get_repo(self, repo_cls: Type[TRepo]) -> TRepo:
        raise NotImplementedError

