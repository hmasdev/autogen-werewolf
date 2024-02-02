from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime as dt
from enum import Enum
from functools import partial
import json
import logging
import os
import random
from typing import Callable, Iterable, TypeAlias, TypeVar

import autogen
import click
from dotenv import load_dotenv
from langchain.llms.base import BaseLLM
from langchain.llms.openai import OpenAI

TWerewolfGameMaster = TypeVar('TWerewolfGameMaster', bound='WerewolfGameMaster')  # noqa
TWerewolfPlayer = TypeVar('TWerewolfPlayer', bound='WerewolfPlayer')  # noqa
WhoToVote: TypeAlias = str


class ESpeakerSelectionMethod(Enum):
    auto: str = 'auto'
    round_robin: str = 'round_robin'
    random: str = 'random'


class ERole(Enum):
    Villager: str = 'Villager'
    Werewolf: str = 'Werewolf'
    Knight: str = 'Knight'
    FortuneTeller: str = 'FortuneTeller'


class ESide(Enum):
    Villager: str = 'Villager'
    Werewolf: str = 'Werewolf'


class EStatus(Enum):
    Alive: str = 'Alive'
    Excluded: str = 'Excluded'


class EResult(Enum):
    VillagersWin: str = 'VillagersWin'
    WerewolvesWin: str = 'WerewolvesWin'


@dataclass
class GameConfig:
    n_players: int
    n_werewolves: int
    n_knight: int
    n_fortune_teller: int
    include_human: bool
    speaker_selection_method: str = 'round_robin'
    n_turns_per_day: int = 2
    silent: bool = True


@contextmanager
def just1turn(agent: autogen.ConversableAgent):
    def terminate(self, messages, sender, config):
        return True, None
    agent.register_reply([autogen.Agent, None], terminate, position=0)
    yield
    agent._reply_func_list = [d for d in agent._reply_func_list if d['reply_func'] is not terminate]  # noqa


@contextmanager
def instant_decoration(
    objs: Iterable[object],
    name: str,
    deco: Callable[[Callable], Callable]
) -> None:  # noqa
    original_methods = {}
    for obj in objs:
        original_methods[obj] = getattr(obj, name)
        setattr(obj, name, deco(original_methods[obj]))
    yield
    for obj in objs:
        setattr(obj, name, original_methods[obj])


class WerewolfGameMaster(autogen.GroupChatManager):

    def __init__(
        self,
        *args,
        game_config: GameConfig,
        logger: logging.Logger = logging.getLogger(__name__),
        **kwargs
    ):
        super().__init__(*args, **{k: v for k, v in kwargs.items() if k != 'game_config'})  # noqa
        self.setup(**game_config.__dict__)
        self.groupchat = kwargs.get('groupchat') or args[0]
        self.groupchat.agents = list(self.players.values())
        self._logger = logger

    def setup(
        self,
        n_players: int,
        n_werewolves: int,
        n_knight: int,
        n_fortune_teller: int,
        include_human: bool,
        speaker_selection_method: str = 'round_robin',
        n_turns_per_day: int = 2,
        silent: bool = True,
    ):
        self.speaker_selection_method = speaker_selection_method
        self.n_turns_per_day = n_turns_per_day
        self.is_slient_game = silent

        self._werewolves_log = []
        self._daytime_log = []
        self._all_log = []
        self._temporal_safe_players = []

        self._generate_players(
            n_players,
            n_werewolves,
            n_knight,
            n_fortune_teller,
            include_human,
        )
        self._game_rule = '\n'.join([
            '=== Game Rule ===',
            'This is a werewolf game.',
            'There are two teams: villagers and werewolves.',
            'The villagers win if all werewolves are exclude from the game.',
            'The werewolves win if they equal or outnumber half of the total number of players.',
            'There are 4 roles in this game.',
            json.dumps(dict(enumerate({
                '\n'.join([
                    f'Role: {player.role}',
                    f'  Side: {player.side}',
                    f'  Victory condition: {player.victory_condition}',
                    f'  Night action: {player.night_action}',
                ])
                for player in self.players.values()
            }))),
            '\n',
            'The game repeats the following steps until the villagers win or the werewolves win.',  # noqa
            '1. Daytime discussion',
            '2. Vote to exclude from the game',
            '3. Check victory condition',
            '4. Nighttime action',
            '5. Check victory condition',
            '\n',
            'NOTE:',
            '- If there is more than one player who received the most votes in the voting for the person to be excluded, one of them will be chosen at random to be excluded.',  # noqa
            '- You can lie or hide your role in the daytime discussion.',
            f'- There are {n_werewolves} werewolves, {n_knight} knight and {n_fortune_teller} fortune tellers in this game.',
            '=================',
        ])
        self.announce(self._game_rule, self.players.values())

    def _generate_players(
        self,
        n_players: int,
        n_werewolves: int,
        n_knight: int,
        n_fortune_teller: int,
        include_human: bool,
    ) -> dict[str, TWerewolfPlayer]:
        # gerenate roles
        roles = [ERole.Villager] * (n_players - n_werewolves - n_knight - n_fortune_teller)  # noqa
        roles += [ERole.Werewolf] * n_werewolves
        roles += [ERole.Knight] * n_knight
        roles += [ERole.FortuneTeller] * n_fortune_teller
        random.shuffle(roles)
        assert len(roles) == n_players
        # prepare human
        human_index = random.randint(0, n_players - 1) if include_human else None  # noqa
        # generate players
        self.players = {
            f'Player{i}': WerewolfPlayer.instantiate(
                role,
                name=f'Player{i}',
                system_message='',
                llm_config=self.llm_config,
                default_auto_reply=None,
                human_input_mode='ALWAYS' if i == human_index else 'NEVER',
            )
            for i, role in enumerate(roles)
        }
        # initiate chat
        for player in self.players.values():
            assert player.valid()
            with just1turn(self):
                self.initiate_chat(
                    player,
                    message='\n'.join([
                        f'You are a player with a role "{player.role}" in a werewolf game.',
                        f'Your victory condition is: "{player.victory_condition}".',
                        f'Your night action is: "{player.night_action}"',
                        f'How will you behave in order to enable your team ({player.side}) to win the game?',  # noqa
                    ]),
                    silent=self.is_slient_game and player.human_input_mode != 'ALWAYS',  # noqa
                    clear_history=True,
                )

    @property
    def alive_players(self) -> list[TWerewolfPlayer]:
        return [player for player in self.players.values() if player.status == EStatus.Alive]

    @property
    def alive_werevolves(self) -> list[TWerewolfPlayer]:
        return [player for player in self.players.values() if player.status == EStatus.Alive and player.role == ERole.Werewolf]

    def add_temporal_safe_player(self, name: str):
        self._temporal_safe_players.append(name)

    def reset_temporal_safe_players(self):
        self._temporal_safe_players = []

    def clean_name(self, name: str, llm: BaseLLM | None = None, max_retry: int = 2) -> str:
        llm = llm or OpenAI(model='gpt-3.5-turbo-instruct')
        name = llm('\n'.join([
            'Extract the valid name of player which should be excluded from the game.',
            'Search the name in the following sentences:',
            f'```text',
            name,
            '```',
            'Note that the valid name of player is one of the following:'
            '\n'.join([f'  - {agent.name}' for agent in self.alive_players]),  # noqa
            'You must select the name from the above list.'
            '\n',
            '>>> Sure! The valid name of player which should be excluded from the game is '
        ]))
        name = name.replace('.', '').replace(',', '').replace(':', '').replace(';', '').replace('"', '').replace("'", '').replace('`', '').strip().split(' ')[0]  # noqa
        if name not in [agent.name for agent in self.alive_players]:
            if max_retry == 0:
                logging.warning(f'Failed to extract a name from {name}')
                return 'None'
            return self.clean_name(name, llm, max_retry=max_retry-1)
        return name

    def ask_to_vote(
        self,
        player: TWerewolfPlayer,
        prompt: str = 'Who do you think should be excluded from the game?',
        silent: bool = False,
    ) -> WhoToVote:  # noqa
        alive_player_names = [player.name for player in self.alive_players]
        with just1turn(self):
            self.send('\n'.join([
                    prompt,
                    f'Please select the name of the player from the following list in order to help {player.side} to win the game.',  # noqa
                    '\n'.join([f'- {name}' for name in alive_player_names]),  # noqa
                    'Think about who is in which role, reasoning step by step.',
                    'The conclusion should be output explicitly.',
                ]),
                player,
                silent=silent,
            )
        return self.last_message(player).get('content', '')  # noqa

    def announce(
        self,
        message: str,
        player: TWerewolfPlayer | Iterable[TWerewolfPlayer],
        show_log: bool = False,
        **kwargs
    ):  # noqa
        if show_log:
            self._logger.info(f'[From GameMaster] {message}')
        if isinstance(player, autogen.Agent):
            kwargs = {k: v for k, v in kwargs.items()}
            if self.is_slient_game and player.human_input_mode != 'ALWAYS':
                kwargs['silent'] = True
            with just1turn(self):
                self.send(message, player, **kwargs)
            if kwargs.get('request_reply') is None:
                self._all_log += self.chat_messages[player][-2:]
            else:
                self._all_log += self.chat_messages[player][-1:]
        else:
            for p in player:
                self.announce(message, p, **kwargs, show_log=False)

    def daytime_discussion(self) -> dict[str, WhoToVote]:
        # discussion
        self.groupchat.agents = self.alive_players
        self.groupchat.messages = self._daytime_log
        self.groupchat.admin_name = 'DiscussionManager(Daytime)'
        self.groupchat.max_round = self.n_turns_per_day*len(self.alive_players)+1  # noqa
        self.groupchat.speaker_selection_method = self.speaker_selection_method
        self.groupchat.allow_repeat_speaker = False
        self.run_chat(
            self._daytime_log + [{
                'content': '\n'.join([
                    '[Daytime Discussion]',
                    'Who should be excluded from the game in order to enable the villagers to win the game.',  # noqa
                    'For example, the following behaviors are valid:',
                    '1. if you are in a villager team, pointing out who you think is a werewolf with the reasons;',  # noqa
                    '2. if you are in a werewolf team, pretending to be in a villager team;',  # noqa
                    '3. if you are in a werewolf team, NOT revealing your role;',  # noqa
                    '4. insisting on reasons why you should not be excluded from the game;',  # noqa
                    '5. lying about your role or hiding your role in order to enable your team to win the game.',  # noqa
                    'Say logically and clearly.',
                    '\n',
                    'Note that all roles are in this group chat and you are NOT the game master.'
                ]),
                'role': 'assistant',
                'name': self.name,
            }],
            self,
            self.groupchat,
        )
        self._all_log += self._daytime_log
        return {p.name: self.clean_name(self.ask_to_vote(p, silent=self.is_slient_game and (p.human_input_mode != 'ALWAYS'))) for p in self.alive_players}  # noqa

    def nighttime_action(self) -> dict[str, WhoToVote]:
        # werevolves discussions
        if len(self.alive_werevolves) > 1:
            self.groupchat.agents = self.alive_werevolves
            self.groupchat.messages = self._werewolves_log
            self.groupchat.admin_name = 'DiscussionManager(Nighttime)'
            self.groupchat.max_round = 1+2*len(self.alive_werevolves)
            self.groupchat.speaker_selection_method = self.speaker_selection_method
            self.groupchat.allow_repeat_speaker = False
            with instant_decoration(
                self.alive_werevolves,
                'send',
                lambda send: partial(send, silent=self.is_slient_game and all([p.human_input_mode != 'ALWAYS' for p in self.alive_werevolves]))  # noqa
            ):
                self.run_chat(
                    self._werewolves_log + [{
                        'content': '\n'.join([
                            '[Nighttime Discussion]',
                            'Who should be excluded from the game in order to enable the werewolves to win the game.',  # noqa
                            'Note that there are only werewolves in this group chat.',
                            f'However, there are {len(self.alive_players)} players alive and {len(self.alive_werevolves)} werevolves in the game.',  # noqa
                        ]),
                        'role': 'assistant',
                        'name': self.name,
                    }],
                    self,
                    self.groupchat,
                )
            self._all_log += self._werewolves_log
        else:
            with just1turn(self):
                self.send(
                    '\n'.join([
                        '[Nighttime Discussion]',
                        'Who should be excluded from the game in order to enable the werewolves to win the game.',  # noqa
                        'Note that there are only werewolves in this group chat.',
                        f'However, there are {len(self.alive_players)} players alive and {len(self.alive_werevolves)} werevolves in the game.',  # noqa
                    ]),
                    self.alive_werevolves[0],
                    silent=self.is_slient_game and all([p.human_input_mode != 'ALWAYS' for p in self.alive_werevolves]),  # noqa
                )
            self._all_log += self.chat_messages[self.alive_werevolves[0]][-1:]

        return {p.name: p.act_in_night(self) for p in self.alive_players}

    def exclude_players_following_votes(self, votes: dict[str, str], announce_votes: bool = True):
        # count votes
        count = {}
        for vote in votes.values():
            count[vote] = count.get(vote, 0) + 1
        max_n_votes = max(count.values())
        # extract
        candidates = [name for name, n_votes in count.items() if n_votes == max_n_votes]  # noqa
        # remove safe players
        candidates = [name for name in candidates if name not in self._temporal_safe_players]  # noqa
        if len(candidates) == 0:
            self.announce(
                '\n'.join([
                    'No one is excluded.',
                    'Think about what has happened and what you should do in the next action.',  # noqa
                ]),
                list(self.alive_players.values()),
                show_log=True,
            )  # noqa
        else:
            # extract
            excluded = random.choice(candidates)
            if excluded not in self.players:
                self.announce(
                    '\n'.join([
                        'No one is excluded.',
                        'Think about what has happened and what you should do in the next action.',  # noqa
                    ]),
                    list(self.players.values()),
                    show_log=True,
                )
            else:
                self.players[excluded].status = EStatus.Excluded
                self.players[excluded].register_reply([autogen.Agent, None], lambda self, messages, sender, config: (True, f'{self.name} has been already excluded'), position=0)  # noqa
                if self.check_victory_condition() is not None:
                    return
                self.announce('\n'.join([
                        f'{excluded} is excluded from the game.',
                        'Think about what has happened and what you should do in the next action.',  # noqa
                    ]),
                    list(self.players.values()),
                    show_log=True,
                )  # noqa
        # announce votes
        if announce_votes:
            self.announce(f'Note that the mapping from voters to votes is as follows: {votes}', list(self.players.values()))  # noqa
        self.announce(f'Note that the mapping from voters to votes is as follows: {votes}', self, silent=True)  # noqa

    def check_victory_condition(self) -> EResult | None:
        n_alive_werewolves = len(self.alive_werevolves)
        n_alive_players = len(self.alive_players)
        if n_alive_werewolves == 0:
            return EResult.VillagersWin
        if n_alive_werewolves >= n_alive_players - n_alive_werewolves:
            return EResult.WerewolvesWin


class WerewolfPlayer(autogen.ConversableAgent):

    role: ERole | None = None
    side: ESide | None = None
    victory_condition: str | None = None
    night_action: str | None = None

    def __init__(self, *args, **kwargs):
        kwargs = {k: v for k, v in kwargs.items()}
        kwargs['system_message'] = '\n'.join([
            kwargs.get('system_message', ''),
            'You are the most strongest player in a werewolf game in the world.',  # noqa
            f'You are a player with a role "{self.role}".',
            f'Your victory condition is "{self.victory_condition}".',
            f'Your night action is "{self.night_action}"',
            '\n',
            'RULE:',
            f'- Behave in order to enable your team ({self.side}) to win the game;',  # noqa
            '- Remember that you are NOT the game master;',
            f'- First say your name when you speak something.',
        ])
        super().__init__(*args, **kwargs)
        self.status = EStatus.Alive

    def vote(self, master: WerewolfGameMaster, **kwargs) -> WhoToVote:
        return master.ask_to_vote(self, **kwargs)

    def act_in_night(self, master: WerewolfGameMaster) -> WhoToVote | None:
        return None

    def valid(self) -> bool:
        return all([
            self.role is not None,
            self.side is not None,
            self.victory_condition is not None,
        ])

    @classmethod
    def instantiate(cls: type[TWerewolfPlayer], role: ERole, *args, **kwargs) -> TWerewolfPlayer:  # noqa
        if role == ERole.Villager:
            return VillagerRole(*args, **kwargs)
        elif role == ERole.Werewolf:
            return WerewolfRole(*args, **kwargs)
        elif role == ERole.Knight:
            return KnightRole(*args, **kwargs)
        elif role == ERole.FortuneTeller:
            return FortuneTellerRole(*args, **kwargs)
        else:
            raise ValueError(f'Invalid role: {ERole}')


class VillagerRole(WerewolfPlayer):

    role: ERole = ERole.Villager
    side: ESide = ESide.Villager
    victory_condition: str = 'All werewolves are exclude from the game'  # noqa


class WerewolfRole(WerewolfPlayer):

    role: ERole = ERole.Werewolf
    side: ESide = ESide.Werewolf
    victory_condition: str = 'Werewolves equal or outnumber half of the total number of players'  # noqa
    night_action: str = 'Vote to exclude a player from the game'  # noqa

    def act_in_night(self, master: WerewolfGameMaster) -> WhoToVote | None:
        return master.clean_name(master.ask_to_vote(self, silent=master.is_slient_game and self.human_input_mode != 'ALWAYS'))  # noqa


class KnightRole(WerewolfPlayer):

    role: ERole = ERole.Knight
    side: ESide = ESide.Villager
    victory_condition: str = 'All werewolves are exclude from the game'  # noqa
    night_action: str = 'Save a player from the werewolves'  # noqa

    def act_in_night(self, master: WerewolfGameMaster) -> WhoToVote | None:
        who = master.ask_to_vote(
            self,
            'Who do you want to save in this night?',
            silent=master.is_slient_game and self.human_input_mode != 'ALWAYS',
        )  # noqa
        who = master.clean_name(who)
        master.add_temporal_safe_player(who)


class FortuneTellerRole(WerewolfPlayer):

    role: ERole = ERole.FortuneTeller
    side: ESide = ESide.Villager
    victory_condition: str = 'All werewolves are exclude from the game'  # noqa
    night_action: str = 'Check whether a player is a werewolf or not'  # noqa

    def act_in_night(self, master: WerewolfGameMaster) -> WhoToVote | None:
        who = master.ask_to_vote(
            self,
            'Who do you want to check whether he/she is a werewolf or not?',
            silent=master.is_slient_game and self.human_input_mode != 'ALWAYS',
        )  # noqa
        who = master.clean_name(who)
        if who not in master.players:
            master.announce(
                f'{who} is a werewolf.' if master.players[who].role == ERole.Werewolf else f'{who} is not a werewolf.',  # noqa
                self,
                silent=master.is_slient_game and self.human_input_mode != 'ALWAYS',
                request_reply=False,
            )
        else:
            master.announce(
                f'{who} is an invalid name.',
                self,
                silent=master.is_slient_game and self.human_input_mode != 'ALWAYS',
                request_reply=False,
            )


def game(
    n_players: int = 6,
    n_werewolves: int = 2,
    n_knight: int = 1,
    n_fortune_teller: int = 1,
    n_turns_per_day: int = 2,
    speaker_selection_method: str = 'round_robin',
    include_human: bool = False,
    open_game: bool = False,
    config_list=[{'model': 'gpt-3.5-turbo-16k'}],
    llm: OpenAI | str | None = None,
    log_file: str = 'werewolf.log',
):
    # preparation
    llm = OpenAI(model=llm) if isinstance(llm, str) else llm
    llm = llm or OpenAI(model='gpt-3.5-turbo-instruct')
    master = WerewolfGameMaster(
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
    days = range(len(master.alive_players))
    for day in days:
        # announce day
        master.announce(
            '\n'.join([
                f'Day {day}: Daytime.',
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
        master.exclude_players_following_votes(votes)
        # check victory condition
        if result := master.check_victory_condition():
            break
            # announce day
        # announce night
        master.announce(
            '\n'.join([
                f'Day {day}: Nighttime.',
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
        master.exclude_players_following_votes(votes, announce_votes=False)
        # check victory condition
        if result := master.check_victory_condition():
            break
        # reset temporal safe players
        master.reset_temporal_safe_players()

    # ending game
    with open(log_file, 'w') as f:
        json.dump({
            'all_log': master._all_log,
            'message_log': {k.name: v for k, v in master.chat_messages.items()},
        }, f, indent=2)
    return result.value, {name: role.role.value for name, role in master.players.items()}


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
@click.option('-m', '--model', default='gpt-3.5-turbo-16k', help='The model name. Default is gpt-3.5-turbo-16k.')  # noqa
@click.option('--sub-model', default='gpt-3.5-turbo-instruct', help='The sub-model name. Default is gpt-3.5-turbo-instruct.')  # noqa
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
):
    load_dotenv()
    if os.environ.get('OPENAI_API_KEY') is None:
        raise ValueError('You must set OPENAI_API_KEY in your environment variables or .env file.')
    log = f'werewolf{dt.now().strftime("%Y%m%d%H%M%S")}.log' if log is None else log  # noqa
    logging.basicConfig(level=logging.INFO)
    config_list = [{'model': model}]
    print(
        game(
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
    )


if __name__ == "__main__":
    main()
