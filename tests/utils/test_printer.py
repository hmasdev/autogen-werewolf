import pytest
from werewolf.utils.printer import (
    _print_dict,
    create_print_func,
)


@pytest.mark.parametrize(
    'key,expected',
    list(_print_dict.items()),
)
def test_create_print_func(key, expected):
    assert create_print_func(key) is expected


def test_create_print_func_invalid_key():
    with pytest.raises(ValueError):
        create_print_func('invalid_key')
