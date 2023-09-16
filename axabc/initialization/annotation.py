import inspect


def get_initializable_annotations(cls, subclass, *, raise_if_not_class=True, raise_on_not_class=True):
    for name_, type_ in cls.__annotations__.items():
        if not inspect.isclass(type_) and raise_if_not_class:
            raise NotImplementedError(f"`{type_}` isn't class, for initializable annotation")

        if not issubclass(type_, subclass) and raise_on_not_class:
            raise NotImplementedError(f"`{type_}` isn't subclass of `{subclass}`, for initializable annotation")

        yield (name_, type_)

