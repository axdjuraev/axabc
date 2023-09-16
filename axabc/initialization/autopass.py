import inspect
from typing import Callable, Iterable, Optional


class AutoPass:
    def __init__(self, recursion_depth=0, max_recursion=1) -> None:
        self.depth = recursion_depth
        self.max_recursion = max_recursion

    def pass_(self, callable: Callable, kwargs: Optional[dict] = None, args: Iterable = tuple()):
        kwargs = kwargs or {}
        parameters = inspect.signature(callable).parameters.values()
        values = {}

        for param in parameters:
            value = self._find_param_value(param, args, kwargs, self.depth, self.max_recursion)

            if value is inspect._empty:
                raise ValueError(f'Could not find value for parameter (`{callable.__name__}.{param.name}:{param.annotation}`)')

            values[param.name] = value

        kwargs_start_index = self._get_signature_kwargs_start_index(parameters)
        args = list(values.values())[:kwargs_start_index]
        kwargs = dict(tuple(values.items())[kwargs_start_index:])

        return callable(*args, **kwargs)

    def _get_signature_kwargs_start_index(self, parameters: Iterable[inspect.Parameter]):
        for index, param in enumerate(parameters):
            if param.kind in (param.KEYWORD_ONLY, param.POSITIONAL_OR_KEYWORD):
                return index

        return None

    def _find_param_value(self, param: inspect.Parameter, args: Iterable, kwargs: dict, depth: int, max_depth: int):
        if param.name in kwargs:
            return kwargs[param.name]
        elif param.annotation is not inspect._empty and type(param.annotation) is not str:
            if inspect.isclass(param.annotation):
                return self._search_through_args_instance(param, args, depth, max_depth)
            elif hasattr(param.annotation, '__origin__') and param.annotation.__origin__ is type:
                return self._search_through_args_instance(param, args, depth, max_depth)

        return inspect._empty

    def _search_through_args_instance(self, param: inspect.Parameter, args: Iterable, depth: int, max_depth: int):
        founds = []

        for arg in args:
            if isinstance(arg, param.annotation):
                founds.append(arg)

        if not founds:
            if depth > max_depth:
                return inspect._empty

            kwargs = self._get_kwargs(args)
            return self._find_param_value(param, args, kwargs, (depth + 1), max_depth)
        else:
            if len(founds) == 1:
                return founds[-1]
            else:
                return self._get_instance_base_mro(param.annotation, founds)

    def _search_through_args_classes(self, param: inspect.Parameter, args: Iterable):
        founds = []

        for arg in args:
            if inspect.isclass(arg) and issubclass(arg, param.annotation):
                founds.append(arg)

        if not founds:
            return inspect._empty

        if len(founds) == 1:
            return founds[-1]
        else:
            return self._get_class_base_mro(param.annotation, founds)

    def _get_kwargs(self, args):
        kwargs = {}
        for arg in args:
            if hasattr(arg, '__dict__'):
                kwargs.update(arg.__dict__)

        return kwargs

    def _get_class_base_mro(self, cls, variants_cls: Iterable):
        ordered_by_mro = sorted(variants_cls, key=lambda ocls: ocls.mro().index(cls))
        return ordered_by_mro[-1]

    def _get_instance_base_mro(self, cls, variants: Iterable):
        ordered_by_mro = sorted(variants, key=lambda obj: obj.__class__.mro().index(cls), reverse=True)
        return ordered_by_mro[-1]

