import autogen
import pytest
from werewolf.config import GameConfig
from werewolf.const import EGameMaster
from werewolf.game_master.base import BaseGameMaster
from werewolf.game_master.default_game_master import DefaultGameMaster


@pytest.mark.parametrize(
    'kind, kwargs, expected',
    [
        (
            EGameMaster.Default,
            {
                'game_config': GameConfig(
                    n_players=12,
                    n_werewolves=3,
                    n_fortune_teller=1,
                    n_knight=1,
                    include_human=False,
                ),
                'groupchat': autogen.GroupChat(agents=[], messages=[]),
                'name': 'GameMaster',
                'llm_config': False,
            },
            DefaultGameMaster,
        ),
    ]
)
def test_WerewolfGameMaster_instantiate(
    kind: EGameMaster,
    kwargs: dict[str, object],
    expected: type[BaseGameMaster],
) -> None:
    assert isinstance(BaseGameMaster.instantiate(kind, **kwargs), expected)


def test_WerewolfGameMaster_instantiate_invalid_kind() -> None:
    with pytest.raises(ValueError):
        BaseGameMaster.instantiate(None)  # type: ignore
