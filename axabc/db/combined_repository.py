from abc import ABC

from axabc.db.async_repository import AbstractAsyncRepository
from .abstract_uow import AbstractUOW


class CombinedRepository(AbstractAsyncRepository, ABC):
    def __init__(self, uow: AbstractUOW) -> None:
        self.uow = uow

