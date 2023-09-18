from abc import ABC
from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class AbstractRepoCollector(ABC):
    _uow: Optional[Any] = None
    _repos: Optional[dict] = None
    
    @classmethod
    def init_repos(cls):
        raise NotImplementedError

