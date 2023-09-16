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

```
"""

