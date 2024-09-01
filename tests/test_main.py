import os
from click.testing import CliRunner
from dotenv import load_dotenv
import pytest
from werewolf.main import main

load_dotenv()


@pytest.mark.integration
@pytest.mark.long
@pytest.mark.skipif(
    os.getenv("OPENAI_API_KEY") is None,
    reason="OPENAI_API is not set.",
)
def test_main_passthrough():
    runner = CliRunner()
    result = runner.invoke(main, [
        '--n-players', '4',
        '--n-werewolves', '1',
        '--n-knight', '1',
        '--n-fortune-teller', '1',
        '--n-turns-per-day', '1',
        '--speaker-selection-method', 'round_robin',
        '--open-game',
        '--model', 'gpt-4o-mini',
        '--sub-model', 'gpt-4o-mini'
    ])
    if result.exit_code != 0:
        print("Output:", result.output)
        print("Exception:", result.exception)
        print("Exit Code:", result.exit_code)
    assert result.exit_code == 0
