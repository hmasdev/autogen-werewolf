from functools import partial
import json
import logging
from typing import Iterable
import random

import autogen
from langchain_openai import ChatOpenAI

from ..alias import WhoToVote
from .base import BaseGameMaster
from ..base import IWerewolfPlayer
from ..const import (
    EResult,
    ERole,
    EStatus,
    DAYTIME_DISCUSSION_MANAGER_NAME,
    NIGHTTIME_DISCUSSION_MANAGER_NAME
)
from ..config import GameConfig
from ..game_player.base import BaseWerewolfPlayer
from ..utils.autogen_utils import just1turn
from ..utils.openai import create_chat_openai_model
from ..utils.utils import instant_decoration


class DefaultGameMaster(BaseGameMaster):

    def __init__(
        self,
        *args,
        game_config: GameConfig,
        logger: logging.Logger = logging.getLogger(__name__),
        **kwargs
    ):
        super().__init__(*args, **{k: v for k, v in kwargs.items() if k != 'game_config'})  # noqa
        self._logger = logger
        self.setup(**game_config.__dict__)
        # NOTE: __post_init__() must be called manually because self.groupchat.agents is set after __init__  # noqa
        self.groupchat.__post_init__()

    @property
    def day(self) -> int:
        return self._day

    def next_day(self):
        self._day += 1

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
        self._day: int = 1
        self.speaker_selection_method = speaker_selection_method
        self.n_turns_per_day = n_turns_per_day
        self.is_silent_game = silent

        # TODO: refine the type hints
        self._werewolves_log: list[dict[str, str]] = []
        self._daytime_log: list[dict[str, str]] = []
        self._all_log: list[dict[str, str]] = []
        self._temporal_safe_players: list[str] = []

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
            'The werewolves win if they equal or outnumber half of the total number of players.',  # noqa
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
            f'- There are {n_werewolves} werewolves, {n_knight} knight and {n_fortune_teller} fortune tellers in this game.',  # noqa
            '=================',
        ])
        self.announce(self._game_rule, self.players.values())
        self.groupchat.agents = list(self.players.values())

    def _generate_players(
        self,
        n_players: int,
        n_werewolves: int,
        n_knight: int,
        n_fortune_teller: int,
        include_human: bool,
    ) -> None:
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
            f'Player{i}': BaseWerewolfPlayer.instantiate(
                role,
                name=f'Player{i}',
                # Need to notify the player's name in the system message  # noqa
                system_message=f'You are "Player{i}"',
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
                        f'You are a player with a role "{player.role}" in a werewolf game.',  # noqa
                        f'Your victory condition is: "{player.victory_condition}".',  # noqa
                        f'Your night action is: "{player.night_action}"',
                        f'How will you behave in order to enable your team ({player.side}) to win the game?',  # noqa
                    ]),
                    silent=self.is_silent_game and player.human_input_mode != 'ALWAYS',  # noqa
                    clear_history=True,
                )
        return None

    @property
    def alive_players(self) -> list[IWerewolfPlayer]:
        return [player for player in self.players.values() if player.status == EStatus.Alive]  # noqa

    @property
    def alive_werewolves(self) -> list[IWerewolfPlayer]:
        return [player for player in self.players.values() if player.status == EStatus.Alive and player.role == ERole.Werewolf]  # noqa

    def add_temporal_safe_player(self, name: str):
        self._temporal_safe_players.append(name)

    def reset_temporal_safe_players(self):
        self._temporal_safe_players = []

    def _clean_name(self, name: str, llm: ChatOpenAI | str | None = None, max_retry: int = 2) -> str:  # noqa
        llm = create_chat_openai_model(llm)
        name = llm.invoke('\n'.join([
            'Extract the valid name of player which should be excluded from the game.',  # noqa
            'Search the name in the following sentences:',
            '```text',
            name,
            '```',
            'Note that the valid name of player is one of the following:'
            '\n'.join([f'  - {agent.name}' for agent in self.alive_players]),  # noqa
            'You must select the name from the above list.'
            '\n',
            '>>> Sure! The valid name of player which should be excluded from the game is '  # noqa
        ])).content  # type: ignore
        name = name.replace('.', '').replace(',', '').replace(':', '').replace(';', '').replace('"', '').replace("'", '').replace('`', '').strip().split(' ')[0]  # noqa
        if name not in [agent.name for agent in self.alive_players]:
            if max_retry == 0:
                logging.warning(f'Failed to extract a name from {name}')
                return 'None'
            return self._clean_name(name, llm=llm, max_retry=max_retry-1)
        return name

    def ask_to_vote(
        self,
        player: IWerewolfPlayer,
        prompt: str = 'Who do you think should be excluded from the game?',
        silent: bool = False,
    ) -> WhoToVote:  # noqa
        self._logger.debug(f'Ask {player.name} to vote')
        alive_player_names = [player.name for player in self.alive_players]
        with just1turn(self):
            self.send('\n'.join([
                    prompt,
                    f'Please select the name of the player from the following list in order to help {player.side} to win the game.',  # noqa
                    '\n'.join([f'- {name}' for name in alive_player_names]),  # noqa
                    'Think about who is in which role, reasoning step by step.',  # noqa
                    'The conclusion should be output explicitly.',
                ]),
                player,
                silent=silent,
            )
        content: str = self.last_message(player).get('content', '')  # noqa
        return self._clean_name(content)

    def announce(
        self,
        message: str,
        player: IWerewolfPlayer | Iterable[IWerewolfPlayer],  # type: ignore
        show_log: bool = False,
        **kwargs
    ) -> None:
        self._logger.debug('Announce message to players')
        if show_log:
            self._logger.info(f'[From GameMaster] {message}')
        if isinstance(player, autogen.Agent):
            kwargs = {k: v for k, v in kwargs.items()}
            if self.is_silent_game and player.human_input_mode != 'ALWAYS':
                kwargs['silent'] = True
            else:
                kwargs['silent'] = False
            with just1turn(self):
                self.send(message, player, **kwargs)
            if kwargs.get('request_reply') is None:
                self._all_log += self.chat_messages[player][-2:]
            else:
                self._all_log += self.chat_messages[player][-1:]
        else:
            for p in player:
                self.announce(message, p, **kwargs, show_log=show_log)
        return None

    def daytime_discussion(self) -> dict[str, WhoToVote]:
        self._logger.debug('Start daytime discussion')
        # discussion
        self.groupchat.agents = self.alive_players
        self.groupchat.messages = self._daytime_log
        self.groupchat.admin_name = DAYTIME_DISCUSSION_MANAGER_NAME
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
                    'Note that all roles are in this group chat and you are NOT the game master.'  # noqa
                ]),
                'role': 'assistant',
                'name': self.name,
            }],
            self,
            self.groupchat,
        )
        self._all_log += self._daytime_log
        return {p.name: self.ask_to_vote(p, silent=self.is_silent_game and (p.human_input_mode != 'ALWAYS')) for p in self.alive_players}  # noqa

    def nighttime_action(self) -> dict[str, WhoToVote]:
        self._logger.debug('Start nighttime action')
        # werewolves discussions
        if len(self.alive_werewolves) > 1:
            self.groupchat.agents = self.alive_werewolves
            self.groupchat.messages = self._werewolves_log
            self.groupchat.admin_name = NIGHTTIME_DISCUSSION_MANAGER_NAME
            self.groupchat.max_round = 1+2*len(self.alive_werewolves)
            self.groupchat.speaker_selection_method = self.speaker_selection_method  # noqa
            self.groupchat.allow_repeat_speaker = False
            with instant_decoration(
                self.alive_werewolves,
                'send',
                lambda send: partial(send, silent=self.is_silent_game and all([p.human_input_mode != 'ALWAYS' for p in self.alive_werewolves]))  # type: ignore # noqa
            ):
                self.run_chat(
                    self._werewolves_log + [{
                        'content': '\n'.join([
                            '[Nighttime Discussion]',
                            'Who should be excluded from the game in order to enable the werewolves to win the game.',  # noqa
                            'Note that there are only werewolves in this group chat.',  # noqa
                            f'However, there are {len(self.alive_players)} players alive and {len(self.alive_werewolves)} werewolves in the game.',  # noqa
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
                        'Note that there are only werewolves in this group chat.',  # noqa
                        f'However, there are {len(self.alive_players)} players alive and {len(self.alive_werewolves)} werewolves in the game.',  # noqa
                    ]),
                    self.alive_werewolves[0],
                    silent=self.is_silent_game and all([p.human_input_mode != 'ALWAYS' for p in self.alive_werewolves]),  # noqa
                )
            self._all_log += self.chat_messages[self.alive_werewolves[0]][-1:]

        return {
            p.name: ngt_vote
            for p in self.alive_players
            if (ngt_vote := p.act_in_night(self))
        }

    def exclude_players_following_votes(self, votes: dict[str, str], announce_votes: bool = True) -> str:   # noqa
        self._logger.debug('Exclude players following votes')
        # count votes
        count: dict[str, int] = {}
        for vote in votes.values():
            count[vote] = count.get(vote, 0) + 1
        max_n_votes = max(count.values())
        # extract
        candidates = [name for name, n_votes in count.items() if n_votes == max_n_votes]  # noqa
        # remove safe players
        candidates = [name for name in candidates if name not in self._temporal_safe_players]  # noqa
        if len(candidates) == 0:
            result = '\n'.join([
                'No one is excluded.',
                'Think about what has happened and what you should do in the next action.',  # noqa
            ])
            self.announce(
                result,
                list(self.alive_players),
                show_log=True,
            )  # noqa
        else:
            # extract
            excluded = random.choice(candidates)
            if excluded not in self.players:
                self._logger.warning(f'{excluded} is not in the game: {self.players}')  # noqa
                result = '\n'.join([
                    'No one is excluded.',
                    'Think about what has happened and what you should do in the next action.',  # noqa
                ])
                self.announce(
                    result,
                    list(self.players.values()),
                    show_log=True,
                )
            else:
                result = '\n'.join([
                    f'{excluded} is excluded from the game.',
                    'Think about what has happened and what you should do in the next action.',  # noqa
                ])
                self.players[excluded].status = EStatus.Excluded
                self.players[excluded].register_reply([autogen.Agent, None], lambda self, messages, sender, config: (True, f'{self.name} has been already excluded'), position=0)  # noqa
                if self.check_victory_condition() is not None:
                    return result
                self.announce(
                    result,
                    list(self.players.values()),
                    show_log=True,
                )  # noqa

        # announce votes
        content: str = f'Note that the mapping from voters to votes is as follows: {votes}'  # noqa
        if announce_votes:
            self.announce(content, list(self.players.values()))
        self.announce(content, self, silent=True)

        return result

    def check_victory_condition(self) -> EResult | None:
        self._logger.debug('Check victory condition')
        n_alive_werewolves = len(self.alive_werewolves)
        n_alive_players = len(self.alive_players)
        if n_alive_werewolves == 0:
            return EResult.VillagersWin
        if n_alive_werewolves >= n_alive_players - n_alive_werewolves:
            return EResult.WerewolvesWin
        return None
