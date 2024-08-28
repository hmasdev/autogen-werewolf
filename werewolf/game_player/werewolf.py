from ..alias import WhoToVote
from .base import BaseWerewolfPlayer
from ..base import IWerewolfGameMaster
from ..const import ERole, ESide, ESideVictoryCondition


class Werewolf(BaseWerewolfPlayer):

    role: ERole = ERole.Werewolf
    side: ESide = ESide.Werewolf
    victory_condition: str = ESideVictoryCondition.WerewolvesWinCondition.value  # noqa
    night_action: str = 'Vote to exclude a player from the game'  # noqa

    def act_in_night(self, master: IWerewolfGameMaster) -> WhoToVote | None:  # noqa
        return master.ask_to_vote(self, silent=master.is_silent_game and self.human_input_mode != 'ALWAYS')  # noqa
