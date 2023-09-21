from abc import ABC
from typing import Any


class AbstractAsyncRepository(ABC):
    def __init__(self, session: Any) -> None:
        self.session = session

