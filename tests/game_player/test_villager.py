from werewolf.const import ERole, ESide, ESideVictoryCondition
from werewolf.game_player.villager import Villager


def test_Villager_init() -> None:
    player = Villager('name', llm_config=False)
    assert player.role == ERole.Villager
    assert player.side == ESide.Villager
    assert player.victory_condition == ESideVictoryCondition.VillagersWinCondition.value  # noqa
