import os
from dotenv import load_dotenv
import pytest
from werewolf.const import DEFAULT_MODEL, EResult
from werewolf.game import game

load_dotenv()


@pytest.mark.integration
@pytest.mark.long
@pytest.mark.skipif(
    os.getenv("OPENAI_API_KEY") is None,
    reason="OPENAI_API is not set.",
)
def test_game_passthrough():
    actual = game(
        n_players=4,
        n_werewolves=1,
        n_knight=1,
        n_fortune_teller=1,
        n_turns_per_day=1,
        speaker_selection_method='round_robin',
        include_human=False,
        open_game=True,
        config_list=[{'model': DEFAULT_MODEL}],
        llm='gpt-4o-mini',
        log_file='werewolf.log',
    )
    assert actual[0] in {result.value for result in EResult}
