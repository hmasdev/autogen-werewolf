import json
import logging
from typing import Iterable

import autogen
from langchain_core.language_models import BaseChatModel

from .chat_models import create_chat_model
from .const import DEFAULT_MODEL, EGameMaster
from .config import GameConfig
from .game_master.base import BaseGameMaster
from .utils.printer import create_print_func


def game(
    n_players: int = 6,
    n_werewolves: int = 2,
    n_knight: int = 1,
    n_fortune_teller: int = 1,
    n_turns_per_day: int = 2,
    speaker_selection_method: str = 'round_robin',
    include_human: bool = False,
    open_game: bool = False,
    config_list=[{'model': DEFAULT_MODEL}],
    llm: BaseChatModel | str | None = None,
    seed: int | None = None,
    printer: str = 'click.echo',
    log_file: str = 'werewolf.log',
    logger: logging.Logger = logging.getLogger(__name__),
):
    # preparation
    print_func = create_print_func(printer)
    llm = create_chat_model(llm, seed=seed)
    master = BaseGameMaster.instantiate(
        EGameMaster.Default,  # TODO
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        name='GameMaster',
        system_message='\n'.join([
            'You are the game master to proceed the werewolf game.',
            'You can see everyone\'s role.',
            'But you must not reveal anyone\'s role to anyone else.',
        ]),
        llm_config={'config_list': config_list},
        default_auto_reply=None,
        game_config=GameConfig(
            n_players=n_players,
            n_werewolves=n_werewolves,
            n_knight=n_knight,
            n_fortune_teller=n_fortune_teller,
            include_human=include_human,
            n_turns_per_day=n_turns_per_day,
            speaker_selection_method=speaker_selection_method,
            silent=not open_game,
        ),
    )

    # start game
    # check victory condition before starting the game
    # TODO: refactor
    days: Iterable[int]
    if result := master.check_victory_condition():
        logger.warning('The game is already finished.')
        days = []
    else:
        days = range(len(master.alive_players))
    for _ in days:
        # announce day
        print_func(f'=============================== Day {master.day} (Daytime) ================================')  # noqa
        master.announce(
            '\n'.join([
                f'Day {master.day}: Daytime.',
                f'Alive players: {[player.name for player in master.alive_players]}',  # noqa
                'Get it?',
            ]),
            list(master.players.values()),
            silent=False,
            show_log=True,
        )
        # daytime discussion
        votes = master.daytime_discussion()
        # exclude from the game
        excluded_result = master.exclude_players_following_votes(votes)
        print_func('\n'.join([
            '============================== Excluded result ==============================',  # noqa
            str(excluded_result),
            '=============================================================================',  # noqa
            json.dumps(votes),
            '=============================================================================',  # noqa
        ]))
        # check victory condition
        if result := master.check_victory_condition():
            break
            # announce day
        # announce night
        print_func(f'================================ Day {master.day} (Nighttime) ================================')  # noqa
        master.announce(
            '\n'.join([
                f'Day {master.day}: Nighttime.',
                f'Alive players: {[player.name for player in master.alive_players]}',  # noqa
                'Get it?',
            ]),
            list(master.players.values()),
            silent=False,
            show_log=True,
        )
        # nighttime action
        votes = master.nighttime_action()
        # exclude from the game
        excluded_result = master.exclude_players_following_votes(votes, announce_votes=False)  # noqa
        print_func('\n'.join([
            '============================== Excluded result ==============================',  # noqa
            str(excluded_result),
            '=============================================================================',  # noqa
        ]))
        # check victory condition
        if result := master.check_victory_condition():
            break
        # reset temporal safe players
        master.reset_temporal_safe_players()

        # next day
        master.next_day()

    # ending game
    with open(log_file, 'w') as f:
        json.dump({
            'all_log': master._all_log,
            'message_log': {k.name: v for k, v in master.chat_messages.items()},  # noqa
        }, f, indent=2)

    if result is None:
        raise ValueError('The game result is invalid.')

    return (
        result.value,
        {
            name: {
                'role': role.role.value,
                'status': role.status,
            }
            for name, role in master.players.items()
            if role.valid()
        },
    )
