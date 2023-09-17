
from typing import Callable
from autopass import AutoPass

class SomeModel1:
    def __init__(self, magic: Callable[[int, str], float]):
        print(magic == really_magic)

def magic(a: int, b: str) -> float: ...

def lie(a: int, b: float) -> float: ...

def lie2(a: int, b: int) -> float: ...

really_magic = magic

AutoPass().pass_(SomeModel1, kwargs={'lie': lie, 'lie2': lie2, 'magic': magic})
