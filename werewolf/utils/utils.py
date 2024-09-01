from contextlib import contextmanager
from typing import Callable, Generator, Iterable, TypeVar

InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')


@contextmanager  # type: ignore
def instant_decoration(
    objs: Iterable[object],
    name: str,
    deco: Callable[
        [Callable[[InputType], OutputType]],
        Callable[[InputType], OutputType]
    ],
) -> Generator[None, None, None]:
    """Decorate a method of multiple objects temporarily.

    Args:
        objs (Iterable[object]): objects to decorate
        name (str): method name to decorate
        deco (Callable[[Callable[[InputType], OutputType]], Callable[[InputType], OutputType] ]): decorator function
    """  # noqa

    original_methods: list[Callable[[InputType], OutputType]] = []
    for obj in objs:
        original_methods.append(getattr(obj, name))  # type: ignore
        setattr(obj, name, deco(original_methods[-1]))
    yield
    for obj, method in zip(objs, original_methods):
        setattr(obj, name, method)


def consecutive_string_generator(
    prefix: str,
    start: int = 0,
    step: int = 1,
) -> Generator[str, None, None]:
    """a generator to generate strings with a prefix and a number.

    Args:
        prefix (str): prefix of the string
        start (int, optional): start number. Defaults to 0.
        step (int, optional): step of the number. Defaults to 1.
    """
    idx = start
    while True:
        yield f'{prefix}{idx}'
        idx += step
