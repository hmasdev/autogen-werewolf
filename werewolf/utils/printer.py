from functools import partial
import logging
from typing import Callable
import click


_print_dict: dict[str, Callable[..., None]] = {
    'print': print,
    'click.echo': click.echo,
    'logging.info': logging.info,
}

KEYS_FOR_PRINTER: tuple[str, ...] = tuple(_print_dict.keys())


def create_print_func(key: str, **kwargs) -> Callable[..., None]:
    """Create a print function.

    Args:
        key (str): key of the print function
        **kwargs: keyword arguments to pass to the print function

    Returns:
        Callable[..., None]: print function
    """
    try:
        if kwargs:
            return partial(_print_dict[key], **kwargs)
        return _print_dict[key]
    except KeyError:
        raise ValueError(f'Invalid key: {key}. Valid keys are {list(KEYS_FOR_PRINTER)}')  # noqa
