from pytest_mock import MockerFixture
from werewolf.utils.utils import instant_decoration


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
