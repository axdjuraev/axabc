from typing import Generic, TypeVar, TYPE_CHECKING


TPrimaryType = TypeVar('TPrimaryType')


class TypeCheat(Generic[TPrimaryType]):
    PrimaryType: type[TPrimaryType]

    __abstract__ = True

    if TYPE_CHECKING:
        from typing import Self

    def __new__(cls, *args, **kwargs) -> 'Self':
        is_abstract = getattr(cls.__dict__, '__abstract__', False)
        print(f'{is_abstract=}; {cls.PrimaryType=}')

        if getattr(cls.__dict__, '__abstract__', False):
            return super().__new__(cls)

        return cls.PrimaryType(*args, **kwargs)  # type: ignore

    def __init_subclass__(cls) -> None:
        if getattr(cls.__dict__, '__abstract__', False):
            return

        cls_name = cls.__new__

        if (
            not (bases := getattr(cls, "__orig_bases__"))
            or not (generics := getattr(bases[0], '__args__'))
        ):
            raise RuntimeError(
                f"Can't create fake type for {cls.__name__}"
                "because it doesn't have any generic parameters"
                "Use Example:\n"
                f"class Some{cls_name}({cls_name}[SomeType]):\n\tpass"
            )

        cls.PrimaryType: type[TPrimaryType] = generics[-1]

