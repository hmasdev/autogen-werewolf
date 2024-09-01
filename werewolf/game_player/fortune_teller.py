from ..alias import WhoToVote
from .base import BaseWerewolfPlayer
from ..base import IWerewolfGameMaster
from ..const import ERole, ESide, ESideVictoryCondition


class FortuneTeller(BaseWerewolfPlayer):

    role: ERole = ERole.FortuneTeller
    side: ESide = ESide.Villager
    victory_condition: str = ESideVictoryCondition.VillagersWinCondition.value  # noqa
    night_action: str = 'Check whether a player is a werewolf or not'  # noqa

    def act_in_night(self, master: IWerewolfGameMaster) -> WhoToVote | None:

        who = master.ask_to_vote(
            self,
            'Who do you want to check whether he/she is a werewolf or not?',  # noqa
            silent=master.is_silent_game and self.human_input_mode != 'ALWAYS',  # noqa
        )

        alive_players_dic = {
            player.name: player
            for player in master.alive_players
        }

        if who in alive_players_dic:
            master.announce(
                f'{who} is a werewolf.' if alive_players_dic[who].role == ERole.Werewolf else f'{who} is not a werewolf.',  # noqa
                self,
                silent=master.is_silent_game and self.human_input_mode != 'ALWAYS',  # noqa
                request_reply=False,
            )
        else:
            master.announce(
                f'{who} is an invalid name.',
                self,
                silent=master.is_silent_game and self.human_input_mode != 'ALWAYS',  # noqa
                request_reply=False,
            )

        return None
