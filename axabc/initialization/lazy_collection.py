from abc import ABC
from typing import Any, Optional
from autopass import AutoPass
from axabc.initialization.annotation import get_initializable_annotations


class LazyInitializableCollection(ABC):
    BaseItemClass: Optional[Any] = None
    use_previous: bool = True

    @classmethod
    def create(
        cls,
        args: Optional[list] = None,
        kwargs: Optional[dict] = None,
        apass: Optional[AutoPass] = None,
    ):
        args = args or []
        apass = apass or AutoPass()
        self = apass.pass_(cls, kwargs, args)

        for name_, type_ in get_initializable_annotations(cls, cls.BaseItemClass):
            args_, kwargs_ = apass.retrieve(type_, kwargs, args)
            setattr(self, name_, type_(*args_, **kwargs_))

            if cls.use_previous:
                args.append(getattr(self, name_))

        return (self, args, kwargs)

