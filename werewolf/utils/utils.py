from contextlib import contextmanager
from functools import partial
from logging import Logger, getLogger
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


def deprecate(
    func: Callable[[InputType], OutputType] | None = None,
    *,
    msg: str = '',
    logger: Logger = getLogger(__name__),
) -> (
    Callable[[InputType], OutputType]
    | Callable[[Callable[[InputType], OutputType]], Callable[[InputType], OutputType]]  # noqa
):
    """Decorator to deprecate a function.

    Args:
        func (Callable[[InputType], OutputType] | None, optional): function to deprecate. Defaults to None.
        msg (str, optional): message to show. Defaults to ''.
        logger (Logger, optional): logger. Defaults to getLogger(__name__).

    Returns:
        Callable[[InputType], OutputType] | Callable[[Callable[[InputType], OutputType]], Callable[[InputType], OutputType]]: decorated function or decorator
    """  # noqa

    if func is None:
        return partial(deprecate, msg=msg, logger=logger)  # type: ignore

    def wrapper(*args, **kwargs):
        if hasattr(func, '__name__'):
            logger.warning(' '.join([f'{func.__name__} is planned to be deprecated.', msg]))  # noqa
        else:
            logger.warning(' '.join([f'{func} is planned to be deprecated.', msg]))  # noqa
        return func(*args, **kwargs)

    return wrapper
