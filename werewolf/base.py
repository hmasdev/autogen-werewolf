from abc import ABC, abstractmethod
from typing import Iterable, TypeVar
import autogen
from .alias import WhoToVote
from .const import EResult, ERole, ESide, EStatus

TIWerewolfGameMaster = TypeVar('TIWerewolfGameMaster', bound='IWerewolfGameMaster')  # noqa
TIWerewolfPlayer = TypeVar('TIWerewolfPlayer', bound='IWerewolfPlayer')  # noqa


class IWerewolfGameMaster(ABC, autogen.GroupChatManager):

    @abstractmethod
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
        raise NotImplementedError()

    @property
    @abstractmethod
    def alive_players(self) -> list[TIWerewolfPlayer]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def alive_werewolves(self) -> list[TIWerewolfPlayer]:
        raise NotImplementedError()

    @abstractmethod
    def ask_to_vote(
        self,
        player: TIWerewolfPlayer,
        prompt: str = 'Who do you think should be excluded from the game?',
        silent: bool = False,
    ) -> WhoToVote:
        raise NotImplementedError()

    @abstractmethod
    def announce(
        self,
        message: str,
        player: TIWerewolfPlayer | Iterable[TIWerewolfPlayer],
        show_log: bool = False,
        **kwargs,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def daytime_discussion(self) -> dict[str, WhoToVote]:
        raise NotImplementedError()

    @abstractmethod
    def nighttime_action(self) -> dict[str, WhoToVote]:
        raise NotImplementedError()

    @abstractmethod
    def exclude_players_following_votes(self, votes: dict[str, str], announce_votes: bool = True) -> str:   # noqa
        raise NotImplementedError()

    @abstractmethod
    def add_temporal_safe_player(self, name: str):
        raise NotImplementedError()

    @abstractmethod
    def reset_temporal_safe_players(self):
        raise NotImplementedError()

    @abstractmethod
    def check_victory_condition(self) -> EResult | None:
        raise NotImplementedError()


class IWerewolfPlayer(ABC, autogen.ConversableAgent):

    role: ERole | None = None
    side: ESide | None = None
    victory_condition: str | None = None
    night_action: str | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status: EStatus = EStatus.Alive
        self.note: str = ''

    @abstractmethod
    def vote(self, master: TIWerewolfGameMaster, **kwargs) -> WhoToVote:
        raise NotImplementedError()

    @abstractmethod
    def act_in_night(self, master: TIWerewolfGameMaster) -> WhoToVote | None:
        raise NotImplementedError()

    @abstractmethod
    def valid(self) -> bool:
        raise NotImplementedError()
