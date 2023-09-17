"""
```python

>>> from pydantic import BaseModel
>>> from axabc.initialization.autopass import AutoPass
>>> autopass = AutoPass()
>>> apass = autopass.pass_ 


## Basic Tests
>>> def a(a: int, b, c):
...     print('   ', [a, b, c])

>>> apass(a, kwargs={'a': 1, 'b': 2, 'c': 3})
    [1, 2, 3]
>>> apass(a, kwargs={'b': 2, 'c': 3}, args=[1])
    [1, 2, 3]
>>> apass(a, kwargs={'b': 2, 'c': 3})
    [3, 2, 3]


## Args Position Tests
>>> class SomeSettings(BaseModel):
...     ...
>>> class SomeSettings2(BaseModel):
...     ...
>>> def requries_settings(settings1: SomeSettings, settings2: SomeSettings2):
...     print(type(settings1).__name__, type(settings2).__name__)

>>> apass(requries_settings, args=[SomeSettings2(), SomeSettings()])
SomeSettings SomeSettings2



## Recursivly Getting from obj Tests
>>> class SomeModel(BaseModel):
...     name: str = 'americano'
...     age: int = 36

>>> def magic(name: str, age: int):
...     print(type(name) is str and type(age) is int)

>>> apass(magic, args=[SomeModel()])
True




## ClassType Requirements Tests
>>> from typing import Type

>>> class SomeModel1(BaseModel):
...     pass

>>> class SomeModel2(BaseModel):
...     pass

>>> def magic(req1: Type[SomeModel1], req2: Type[SomeModel2]):
...     print(req1 is SomeModel1 and req2 is SomeModel2)

>>> apass(magic, args=[SomeModel1, SomeModel2])
True




## Test Callable pass
>>> from typing import Callable
>>> class SomeModel1:
...     def __init__(self, magic: Callable[[int, str], float]):
...         print(magic == real_magic)

>>> def magic(a: int, b: str) -> float:
...     print(req1 is SomeModel1 and req2 is SomeModel2)

>>> def lie(a: int, b: float) -> float:
...     print(req1 is SomeModel1 and req2 is SomeModel2)

>>> def lie2(a: int, b: int) -> float:
...     print(req1 is SomeModel1 and req2 is SomeModel2)

>>> real_magic = magic

>>> _ = apass(SomeModel1, kwargs={'lie': lie, 'lie2': lie2, 'magic': magic})
True




## Test Callable pass through recursive
>>> from typing import Callable
>>> class SomeModel:
...     def __init__(self, logger):
...         print(magic == real_magic)
>>> class SomeModel1:
...     def __init__(self, magic: Callable[[int, str], float]):
...         print(magic == real_magic)

>>> def magic(a: int, b: str) -> float:
...     print(req1 is SomeModel1 and req2 is SomeModel2)

>>> def lie(a: int, b: float) -> float:
...     print(req1 is SomeModel1 and req2 is SomeModel2)

>>> def lie2(a: int, b: int) -> float:
...     print(req1 is SomeModel1 and req2 is SomeModel2)

>>> real_magic = magic

>>> _ = apass(SomeModel1, kwargs={'lie': lie, 'lie2': lie2, 'magic': magic})
True




# LazyInitializableCollection Tests
>>> from abc import ABC
>>> from axabc.initialization.lazy_collection import LazyInitializableCollection
>>> from axabc.logging.simple_file_logger import SimpleFileLogger

>>> class BaseSettings(ABC):
...     def __init__(self, logger: SimpleFileLogger):
...         self.logger = logger


>>> class Settings1(BaseSettings): ...


>>> class Settings2(BaseSettings):
...     def __init__(self, logger: SimpleFileLogger, magic: Settings1):
...         self.logger = logger
...         self.magic = magic


>>> class Settings3(BaseSettings):
...     def __init__(self, logger: SimpleFileLogger, magic: Settings2):
...         self.logger = logger
...         self.magic = magic


>>> class SettingsCollection(LazyInitializableCollection):
...     settings1: Settings1
...     settings2: Settings2
...     settings3: Settings3

>>> logger = SimpleFileLogger('really simple')

>>> settings_collection, _, _ = SettingsCollection.create(args=[logger])

>>> print(
...     type(settings_collection.settings3) is Settings3, 
...     type(settings_collection.settings1) is Settings1,
... )
True True

```
"""

