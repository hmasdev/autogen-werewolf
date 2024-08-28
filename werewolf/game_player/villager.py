from .base import BaseWerewolfPlayer
from ..const import ERole, ESide, ESideVictoryCondition


class Villager(BaseWerewolfPlayer):

    role: ERole = ERole.Villager
    side: ESide = ESide.Villager
    victory_condition: str = ESideVictoryCondition.VillagersWinCondition.value  # noqa
