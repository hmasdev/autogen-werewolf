from datetime import datetime as dt
import logging
import os

import click
from dotenv import load_dotenv

from .const import DEFAULT_MODEL, ESpeakerSelectionMethod
from .game import game


@click.command()
@click.option('-n', '--n-players', default=6, help='The number of players. Default is 6.')  # noqa
@click.option('-w', '--n-werewolves', default=2, help='The number of werewolves. Default is 2.')  # noqa
@click.option('-k', '--n-knight', default=1, help='The number of knights. Default is 1.')  # noqa
@click.option('-f', '--n-fortune-teller', default=1, help='The number of fortune tellers. Default is 1.')  # noqa
@click.option('-t', '--n-turns-per-day', default=2, help='The number of turns per day. Default is 2.')  # noqa
@click.option('-s', '--speaker-selection-method', type=ESpeakerSelectionMethod, default=ESpeakerSelectionMethod.round_robin, help='The method to select a speaker. Default is round_robin.')  # noqa
@click.option('-h', '--include-human', is_flag=True, help='Whether to include human or not.')  # noqa
@click.option('-o', '--open-game', is_flag=True, help='Whether to open game or not.')  # noqa
@click.option('-l', '--log', default=None, help='The log file name. Default is werewolf%Y%m%d%H%M%S.log')  # noqa
@click.option('-m', '--model', default=DEFAULT_MODEL, help=f'The model name. Default is {DEFAULT_MODEL}.')  # noqa
@click.option('--sub-model', default=DEFAULT_MODEL, help=f'The sub-model name. Default is {DEFAULT_MODEL}.')  # noqa
@click.option('--log-level', default='WARNING', help='The log level, DEBUG, INFO, WARNING, ERROR or CRITICAL. Default is WARNING.')  # noqa
@click.option('--debug', is_flag=True, help='Whether to show debug logs or not.')  # noqa
def main(
    n_players: int,
    n_werewolves: int,
    n_knight: int,
    n_fortune_teller: int,
    n_turns_per_day: int,
    speaker_selection_method: ESpeakerSelectionMethod,
    include_human: bool,
    open_game: bool,
    log: str,
    model: str,
    sub_model: str,
    log_level: str,
    debug: bool,
):
    load_dotenv(),
    if os.environ.get('OPENAI_API_KEY') is None:
        raise ValueError('You must set OPENAI_API_KEY in your environment variables or .env file.')  # noqa
    log = f'werewolf{dt.now().strftime("%Y%m%d%H%M%S")}.log' if log is None else log  # noqa
    logging.basicConfig(level=logging.DEBUG if debug else getattr(logging, log_level.upper(), 'WARNING'))  # type: ignore # noqa
    config_list = [{'model': model}]
    result = game(
        n_players=n_players,
        n_werewolves=n_werewolves,
        n_knight=n_knight,
        n_fortune_teller=n_fortune_teller,
        n_turns_per_day=n_turns_per_day,
        speaker_selection_method=speaker_selection_method.value,
        include_human=include_human,
        open_game=open_game,
        log_file=log,
        config_list=config_list,
        llm=sub_model,
    )
    click.echo('================================ Game Result ================================')  # noqa
    click.echo(result)


if __name__ == "__main__":
    main()