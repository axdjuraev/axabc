import inspect
from typing import Any, Optional, Type


def get_initializable_annotations(cls, subclass: Optional[Type[Any]] = None, *, raise_if_not_class=True, raise_on_not_class=False):
    for name_, type_ in cls.__annotations__.items():
        if not inspect.isclass(type_):
            if raise_if_not_class:
                raise NotImplementedError(f"`{type_}` isn't class, for initializable annotation")
            continue

        if type_ is subclass:
            continue

        if subclass and not issubclass(type_, subclass):
            if raise_on_not_class:
                raise NotImplementedError(f"`{type_}` isn't subclass of `{subclass}`, for initializable annotation")
            continue

        yield (name_, type_)

