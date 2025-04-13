from datetime import datetime as dt
import logging
import os

import click
from dotenv import load_dotenv

from .const import (
    DEFAULT_MODEL,
    EChatService,
    ESpeakerSelectionMethod,
    MODEL_SERVICE_MAP,
    SERVICE_APIKEY_ENVVAR_MAP,
    VALID_MODELS,
)
from .game import game
from .utils.printer import KEYS_FOR_PRINTER, create_print_func


@click.command()
@click.option('-n', '--n-players', default=6, help='The number of players. Default is 6.')  # noqa
@click.option('-w', '--n-werewolves', default=2, help='The number of werewolves. Default is 2.')  # noqa
@click.option('-k', '--n-knight', default=1, help='The number of knights. Default is 1.')  # noqa
@click.option('-f', '--n-fortune-teller', default=1, help='The number of fortune tellers. Default is 1.')  # noqa
@click.option('-t', '--n-turns-per-day', default=2, help='The number of turns per day. Default is 2.')  # noqa
@click.option('-s', '--speaker-selection-method', type=ESpeakerSelectionMethod, default=ESpeakerSelectionMethod.round_robin, help='The method to select a speaker. Default is round_robin.')  # noqa
@click.option('-h', '--include-human', is_flag=True, help='Whether to include human or not.')  # noqa
@click.option('-o', '--open-game', is_flag=True, help='Whether to open game or not.')  # noqa
@click.option('-l', '--log', default=None, help='The log file name. Default is ./logs/werewolf%Y%m%d%H%M%S.log')  # noqa
@click.option('-m', '--model', default=DEFAULT_MODEL, help=f'The model name. Default is {DEFAULT_MODEL}. The valid model is as follows: {VALID_MODELS} or the repository id of huggingface.')  # noqa
@click.option('-p', '--printer', default='click.echo', help=f'The printer name. The valid values is in {KEYS_FOR_PRINTER}. Default is click.echo.')  # noqa
@click.option('--sub-model', default=DEFAULT_MODEL, help=f'The sub-model name. Default is {DEFAULT_MODEL}. The valid model is as follows: {VALID_MODELS} or the repository id of huggingface')  # noqa
@click.option('--seed', default=-1, help='The random seed. Default to -1. NOTE: a negative integer means "not specify the seed"')  # noqa
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
    printer: str,
    sub_model: str,
    seed: int,
    log_level: str,
    debug: bool,
):
    if seed >= 0:
        import random
        random.seed(seed)

    load_dotenv(override=True)
    if os.environ.get('OPENAI_API_KEY') is None:
        raise ValueError('You must set OPENAI_API_KEY in your environment variables or .env file.')  # noqa

    printer_func = create_print_func(printer)

    log = f'./logs/werewolf{dt.now().strftime("%Y%m%d%H%M%S")}.log' if log is None else log  # noqa
    logging.basicConfig(level=logging.DEBUG if debug else getattr(logging, log_level.upper(), 'WARNING'))  # type: ignore # noqa
    if (service := MODEL_SERVICE_MAP[model]) == EChatService.OpenAI:
        config_list = [{'model': model}]
    else:
        config_list = [{
            'model': model,
            'api_type': service.value,
            # FIXME: this is not good because the raw token is on memory
            'api_key': os.getenv(SERVICE_APIKEY_ENVVAR_MAP[service]),  # type: ignore # noqa
        }]

    result = game(
        n_players=n_players,
        n_werewolves=n_werewolves,
        n_knight=n_knight,
        n_fortune_teller=n_fortune_teller,
        n_turns_per_day=n_turns_per_day,
        speaker_selection_method=speaker_selection_method.value,
        include_human=include_human,
        open_game=open_game,
        printer=printer,
        log_file=log,
        config_list=config_list,
        llm=sub_model,
        seed=seed,
    )

    printer_func('================================ Game Result ================================')  # noqa
    printer_func(result)


if __name__ == "__main__":
    main()
