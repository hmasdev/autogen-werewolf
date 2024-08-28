from pytest_mock import MockerFixture
from werewolf.base import IWerewolfGameMaster
from werewolf.const import ERole, ESide, ESideVictoryCondition
from werewolf.game_player.werewolf import Werewolf


def test_Werewolf_init() -> None:
    player = Werewolf('name', llm_config=False)
    assert player.role == ERole.Werewolf
    assert player.side == ESide.Werewolf
    assert player.victory_condition == ESideVictoryCondition.WerewolvesWinCondition.value  # noqa
    assert player.night_action == 'Vote to exclude a player from the game'  # noqa


def test_Werewolf_act_in_night(mocker: MockerFixture) -> None:
    # setup
    expected = 'dummy'
    master = mocker.MagicMock(IWerewolfGameMaster)
    master.is_silent_game = False
    master.ask_to_vote.return_value = expected
    player = Werewolf('name', llm_config=False)
    # execute
    actual = player.act_in_night(master)
    # assert
    assert actual == expected
