from pytest_mock import MockerFixture
from werewolf.base import IWerewolfGameMaster
from werewolf.const import ERole, ESide, ESideVictoryCondition
from werewolf.game_player.knight import Knight


def test_Knight_init() -> None:
    player = Knight('name', llm_config=False)
    assert player.role == ERole.Knight
    assert player.side == ESide.Villager
    assert player.victory_condition == ESideVictoryCondition.VillagersWinCondition.value  # noqa
    assert player.night_action == 'Save a player from the werewolves'


def test_Knight_act_in_night(mocker: MockerFixture) -> None:
    # setup
    expected = 'dummy'
    master = mocker.MagicMock(IWerewolfGameMaster)
    master.is_silent_game = False
    master.ask_to_vote.return_value = expected
    player = Knight('name', llm_config=False)
    # execute
    player.act_in_night(master)
    # assert
    master.ask_to_vote.assert_called_once()
    master.add_temporal_safe_player.assert_called_once_with(expected)
