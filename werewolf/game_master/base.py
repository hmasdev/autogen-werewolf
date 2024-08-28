from ..base import IWerewolfGameMaster
from ..const import EGameMaster


class BaseGameMaster(IWerewolfGameMaster):

    @classmethod
    def instantiate(
        cls: type[IWerewolfGameMaster],
        kind: EGameMaster,
        *args, **kwargs
    ) -> IWerewolfGameMaster:
        from .default_game_master import DefaultGameMaster
        try:
            return {
                EGameMaster.Default: DefaultGameMaster,
            }[kind](*args, **kwargs)
        except KeyError:
            raise ValueError(f'Unknown game master kind: {kind}')
