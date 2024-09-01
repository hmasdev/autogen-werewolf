from ..alias import WhoToVote
from .base import BaseWerewolfPlayer
from ..base import IWerewolfGameMaster
from ..const import ERole, ESide, ESideVictoryCondition


class Knight(BaseWerewolfPlayer):

    role: ERole = ERole.Knight
    side: ESide = ESide.Villager
    victory_condition: str = ESideVictoryCondition.VillagersWinCondition.value  # noqa
    night_action: str = 'Save a player from the werewolves'  # noqa

    def act_in_night(self, master: IWerewolfGameMaster) -> WhoToVote | None:
        who = master.ask_to_vote(
            self,
            'Who do you want to save in this night?',
            silent=master.is_silent_game and self.human_input_mode != 'ALWAYS',
        )  # noqa
        master.add_temporal_safe_player(who)
        return None
