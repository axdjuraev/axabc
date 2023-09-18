from abc import ABC
from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class AbstractRepoCollector(ABC):
    _repos: Optional[dict] = None
    _uow: Optional[Any] = None
    
    @classmethod
    def init_repos(cls):
        raise NotImplementedError

