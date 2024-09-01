import pytest
from pytest_mock import MockerFixture
from werewolf.base import IWerewolfGameMaster
from werewolf.game_player.base import BaseWerewolfPlayer
from werewolf.game_player.fortune_teller import FortuneTeller
from werewolf.game_player.knight import Knight
from werewolf.game_player.villager import Villager
from werewolf.game_player.werewolf import Werewolf
from werewolf.const import ERole, ESide, ESideVictoryCondition, EStatus


@pytest.mark.parametrize(
    'role, expected',
    [
        (ERole.Werewolf, Werewolf),
        (ERole.Knight, Knight),
        (ERole.FortuneTeller, FortuneTeller),
        (ERole.Villager, Villager),
    ]
)
def test_BaseWerewolfPlayer_instantiate(
    role: ERole,
    expected: type[BaseWerewolfPlayer]
) -> None:
    assert isinstance(BaseWerewolfPlayer.instantiate(
        role,
        'name',
        llm_config=False,
    ), expected)  # noqa


def test_BaseWerewolfPlayer_instantiate_invalid_role() -> None:
    with pytest.raises(ValueError):
        BaseWerewolfPlayer.instantiate(None, 'name')  # type: ignore


def test_BaseWerewolfPlayer_init() -> None:
    system_message = 'dummy'
    player = BaseWerewolfPlayer('name', llm_config=False, system_message=system_message)  # noqa
    assert 'RULE:' not in system_message and 'RULE:' in player.system_message
    assert player.status == EStatus.Alive
    assert player.note == ''


def test_BaseWerewolfPlayer_vote(mocker: MockerFixture) -> None:
    master = mocker.MagicMock(IWerewolfGameMaster)
    master.ask_to_vote.return_value = 'dummy'
    player = BaseWerewolfPlayer('name', llm_config=False)
    assert player.vote(master) == master.ask_to_vote.return_value


def test_BaseWerewolfPlayer_act_in_night(mocker: MockerFixture) -> None:
    master = mocker.MagicMock(IWerewolfGameMaster)
    player = BaseWerewolfPlayer('name', llm_config=False)
    assert player.act_in_night(master) is None


def test_BaseWerewolfPlayer_valid() -> None:
    player = BaseWerewolfPlayer('name', llm_config=False)
    assert not player.valid()
    player.role = ERole.Werewolf
    assert not player.valid()
    player.side = ESide.Werewolf
    assert not player.valid()
    player.victory_condition = ESideVictoryCondition.WerewolvesWinCondition.value  # noqa
    assert player.valid()
