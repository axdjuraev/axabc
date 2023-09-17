import inspect
from typing import Any, Callable, Iterable, Optional
from typing import _CallableGenericAlias  # type: ignore


class AutoPass:
    def __init__(self, recursion_depth=0, max_recursion=1) -> None:
        self.depth = recursion_depth
        self.max_recursion = max_recursion

    def retrieve(self, callable: Callable, kwargs: Optional[dict] = None, args: Iterable = tuple()) -> tuple[list, dict]:
        kwargs = kwargs or {}
        args = list(args)
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

        return args, kwargs

    def pass_(self, callable: Callable, kwargs: Optional[dict] = None, args: Iterable = tuple()):
        args, kwargs = self.retrieve(callable, kwargs, args)

        return callable(*args, **kwargs)

    def _get_signature_kwargs_start_index(self, parameters: Iterable[inspect.Parameter]):
        for index, param in enumerate(parameters):
            if param.kind in (param.KEYWORD_ONLY, param.POSITIONAL_OR_KEYWORD):
                return index

        return None

    def _find_param_value(
        self,
        param: inspect.Parameter,
        args: Iterable,
        kwargs: dict,
        depth: int,
        max_depth: int,
        strict: bool = False,
    ):
        if param.name in kwargs and not strict:
            return kwargs[param.name]

        elif param.annotation is not inspect._empty and type(param.annotation) is not str:
            args = (*kwargs.values(), *args)
            if type(param.annotation) is _CallableGenericAlias:
                return self._search_callable(param, args, kwargs, depth, max_depth)
            if hasattr(param.annotation, '__origin__') and param.annotation.__origin__ is type:
                return self._search_through_args_classes(param, args)
            elif inspect.isclass(param.annotation):
                return self._search_through_args_instance(param, args, depth, max_depth)

        return inspect._empty

    def _search_callable(self, param: inspect.Parameter, args, kwargs: dict, depth: int, max_depth: int):
        found = kwargs.get(param.name)
        if not found or not isinstance(found, Callable):
            if depth > max_depth:
                return inspect._empty

            kwargs = self._get_kwargs(args)
            return self._find_param_value(param, args, kwargs, (depth + 1), max_depth, strict=True)

        sign = inspect.signature(found)
        sign_annotations = map(lambda s: s.annotation, sign.parameters.values())
        callable_reqs = param.annotation.__args__
        callable_reqs_len = len(callable_reqs)

        for index, annot in enumerate(sign_annotations):
            if callable_reqs_len < (index + 1):
                break
            if callable_reqs_len == (index + 1):
                annot = sign.return_annotation
            if callable_reqs[index] is Any:
                continue
            if annot is param.empty or not issubclass(annot, callable_reqs[index]):
                return param.empty

        return found

    def _search_through_args_instance(self, param: inspect.Parameter, args: Iterable, depth: int, max_depth: int):
        founds = []

        for arg in args:
            if isinstance(arg, param.annotation):
                founds.append(arg)

        if not founds:
            if depth > max_depth:
                return inspect._empty

            kwargs = self._get_kwargs(args)
            return self._find_param_value(param, args, kwargs, (depth + 1), max_depth, strict=True)

        if len(founds) == 1:
            return founds[-1]
        return self._get_instance_base_mro(param.annotation, founds)

    def _search_through_args_classes(self, param: inspect.Parameter, args: Iterable):
        founds = []

        for arg in args:
            if inspect.isclass(arg) and issubclass(arg, param.annotation.__args__[-1]):
                founds.append(arg)

        if not founds:
            return inspect._empty

        if len(founds) == 1:
            return founds[-1]

        return self._get_class_base_mro(param.annotation, founds)

    def _get_kwargs(self, args):
        kwargs = {}
        for arg in args:
            if hasattr(arg, '__dict__'):
                kwargs.update(arg.__dict__)
            if hasattr(arg, '__dir__'):
                for name in dir(arg):
                    if name.startswith('__'):
                        continue

                    val = getattr(arg, name)

                    if isinstance(val, Callable):
                        kwargs[name] = val

        return kwargs

    def _get_class_base_mro(self, cls, variants_cls: Iterable):
        ordered_by_mro = sorted(variants_cls, key=lambda ocls: ocls.mro().index(cls))
        return ordered_by_mro[-1]

    def _get_instance_base_mro(self, cls, variants: Iterable):
        ordered_by_mro = sorted(variants, key=lambda obj: obj.__class__.mro().index(cls), reverse=True)
        return ordered_by_mro[-1]

