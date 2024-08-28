from ..alias import WhoToVote
from ..base import IWerewolfPlayer, IWerewolfGameMaster
from ..const import ERole, ESide, EStatus


class BaseWerewolfPlayer(IWerewolfPlayer):

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
            '- First say your name when you speak something.',
        ])
        super().__init__(*args, **kwargs)
        self.status: EStatus = EStatus.Alive
        self.note: str = ''

    def vote(self, master: IWerewolfGameMaster, **kwargs) -> WhoToVote:
        return master.ask_to_vote(self, **kwargs)

    def act_in_night(self, master: IWerewolfGameMaster) -> WhoToVote | None:
        return None

    def valid(self) -> bool:
        return all([
            self.role is not None,
            self.side is not None,
            self.victory_condition is not None,
        ])

    @classmethod
    def instantiate(
        cls: type[IWerewolfPlayer],
        role: ERole,
        *args, **kwargs,
    ) -> IWerewolfPlayer:
        from .fortune_teller import FortuneTeller
        from .knight import Knight
        from .villager import Villager
        from .werewolf import Werewolf
        try:
            return {
                ERole.Werewolf: Werewolf,
                ERole.Knight: Knight,
                ERole.FortuneTeller: FortuneTeller,
                ERole.Villager: Villager,
            }[role](*args, **kwargs)
        except KeyError:
            raise ValueError(f'Invalid role: {role}')
