from enum import Enum

DEFAULT_MODEL: str = 'gpt-4o-mini'

DAYTIME_DISCUSSION_MANAGER_NAME: str = 'DiscussionManager(Daytime)'
NIGHTTIME_DISCUSSION_MANAGER_NAME: str = 'DiscussionManager(Nighttime)'

PREFIX_PLAYER_NAME: str = 'Player'


class ESpeakerSelectionMethod(Enum):
    auto: str = 'auto'
    round_robin: str = 'round_robin'
    random: str = 'random'


class EGameMaster(Enum):
    Default: str = 'DefaultGameMaster'


class ERole(Enum):
    Villager: str = 'Villager'
    Werewolf: str = 'Werewolf'
    Knight: str = 'Knight'
    FortuneTeller: str = 'FortuneTeller'


class ESide(Enum):
    Villager: str = 'Villager'
    Werewolf: str = 'Werewolf'


class ESideVictoryCondition(Enum):
    VillagersWinCondition: str = 'All werewolves are exclude from the game'
    WerewolvesWinCondition: str = 'Werewolves equal or outnumber half of the total number of players'  # noqa


class EStatus(Enum):
    Alive: str = 'Alive'
    Excluded: str = 'Excluded'


class EResult(Enum):
    VillagersWin: str = 'VillagersWin'
    WerewolvesWin: str = 'WerewolvesWin'
