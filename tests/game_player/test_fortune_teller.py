import pytest
from pytest_mock import MockerFixture
from werewolf.base import IWerewolfGameMaster
from werewolf.const import ERole, ESide, ESideVictoryCondition
from werewolf.game_player.base import BaseWerewolfPlayer
from werewolf.game_player.fortune_teller import FortuneTeller


def test_FortuneTeller_init() -> None:
    player = FortuneTeller('name', llm_config=False)
    assert player.role == ERole.FortuneTeller
    assert player.side == ESide.Villager
    assert player.victory_condition == ESideVictoryCondition.VillagersWinCondition.value  # noqa
    assert player.night_action == 'Check whether a player is a werewolf or not'


class _Villager(BaseWerewolfPlayer):
    role: ERole = ERole.Villager

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class _Werewolf(BaseWerewolfPlayer):
    role: ERole = ERole.Werewolf

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@pytest.mark.parametrize(
    'who, alive_players, expected',
    [
        (
            'dummy',
            [_Werewolf('dummy', llm_config=False),],
            'dummy is a werewolf.'
        ),
        (
            'dummy',
            [_Villager('dummy', llm_config=False),],
            'dummy is not a werewolf.'
        ),
        (
            'dummy',
            {},
            'dummy is an invalid name.'
        ),
    ]
)
def test_FortuneTeller_act_in_night(
    who: str,
    alive_players: list[BaseWerewolfPlayer],
    expected: str,
    mocker: MockerFixture,
) -> None:
    # setup
    master = mocker.MagicMock(IWerewolfGameMaster)
    master.is_silent_game = False
    master.ask_to_vote.return_value = who
    master.alive_players = alive_players
    player = FortuneTeller('name', llm_config=False)
    # execute
    player.act_in_night(master)
    # assert
    master.ask_to_vote.assert_called_once()
    master.announce.assert_called_once_with(
        expected,
        player,
        silent=master.is_silent_game and player.human_input_mode != 'ALWAYS',
        request_reply=False,
    )
