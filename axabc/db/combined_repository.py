from abc import ABC
from .abstract_uow import AbstractUOW


class CombinedRepository(ABC):
    def __init__(self, uow: AbstractUOW) -> None:
        self.uow = uow

