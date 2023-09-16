from abc import ABC
from typing import Any, Optional
from axabc.initialization.autopass import AutoPass
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
        apass = apass or AutoPass()
        for name_, type_ in get_initializable_annotations()


