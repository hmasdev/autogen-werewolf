import pytest
from pytest_mock import MockerFixture
from werewolf.utils.utils import (
    instant_decoration,
    consecutive_string_generator,
)


class EchoNameCls:
    def __init__(self, name: str) -> None:
        self.name = name

    def echo_name(self) -> str:
        return self.name


def test_instant_decoration(mocker: MockerFixture) -> None:

    # preparation
    objs = [EchoNameCls('A'), EchoNameCls('B')]
    footer: str = 'decorated'

    def deco(func):
        def wrapper(*args, **kwargs):
            return f'{func(*args, **kwargs)}{footer}'
        return wrapper

    # test
    # expected: each object's echo_name return its name
    #           with the footer in `with` block
    for obj in objs:
        assert obj.echo_name() == obj.name
    with instant_decoration(objs, 'echo_name', deco):
        for obj in objs:
            assert obj.echo_name() == f'{obj.name}{footer}'
    for obj in objs:
        assert obj.echo_name() == obj.name


@pytest.mark.parametrize(
    'prefix, start, step, n, expected',
    [
        ('a', 0, 1, 3, ['a0', 'a1', 'a2']),
        ('b', 1, 2, 4, ['b1', 'b3', 'b5', 'b7']),
    ]
)
def test_consecutive_string_generator(
    prefix: str,
    start: int,
    step: int,
    n: int,
    expected: list[str],
) -> None:
    gen = consecutive_string_generator(prefix, start, step)
    assert [p for _, p in zip(range(n), gen)] == expected
