from dataclasses import dataclass


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
