from enum import Enum

DEFAULT_MODEL: str = 'gpt-4o-mini'

DAYTIME_DISCUSSION_MANAGER_NAME: str = 'DiscussionManager(Daytime)'
NIGHTTIME_DISCUSSION_MANAGER_NAME: str = 'DiscussionManager(Nighttime)'

PREFIX_PLAYER_NAME: str = 'Player'


class ESpeakerSelectionMethod(Enum):
    auto = 'auto'
    round_robin = 'round_robin'
    random = 'random'


class EGameMaster(Enum):
    Default = 'DefaultGameMaster'


class ERole(Enum):
    Villager = 'Villager'
    Werewolf = 'Werewolf'
    Knight = 'Knight'
    FortuneTeller = 'FortuneTeller'


class ESide(Enum):
    Villager = 'Villager'
    Werewolf = 'Werewolf'


class ESideVictoryCondition(Enum):
    VillagersWinCondition = 'All werewolves are exclude from the game'
    WerewolvesWinCondition = 'Werewolves equal or outnumber half of the total number of players'  # noqa


class EStatus(Enum):
    Alive = 'Alive'
    Excluded = 'Excluded'


class EResult(Enum):
    VillagersWin = 'VillagersWin'
    WerewolvesWin = 'WerewolvesWin'


class EChatService(Enum):
    OpenAI = 'openai'
    Google = 'google'
    Groq = 'groq'


MODEL_SERVICE_MAP: dict[str, EChatService] = {
    'gpt-3.5-turbo': EChatService.OpenAI,
    'gpt-4': EChatService.OpenAI,
    'gpt-4-turbo': EChatService.OpenAI,
    'gpt-4o': EChatService.OpenAI,
    'gpt-4o-mini': EChatService.OpenAI,
    'gemini-1.5-flash': EChatService.Google,
    "gemini-pro-vision": EChatService.Google,
    'gemini-pro': EChatService.Google,
    'gemma2-9b-it': EChatService.Groq,
    'gemma2-7b-it': EChatService.Groq,
    'llama3-groq-70b-8192-tool-use-preview': EChatService.Groq,
    'llama3-groq-8b-8192-tool-use-preview': EChatService.Groq,
    'llama-3.1-70b-versatile': EChatService.Groq,
    'llama-3.1-8b-instant': EChatService.Groq,
    'llama-guard-3-8b': EChatService.Groq,
    'llava-v1.5-7b-4096-preview': EChatService.Groq,
    'llama3-70b-8192': EChatService.Groq,
    'llama3-8b-8192': EChatService.Groq,
    'mixtral-8x7b-32768': EChatService.Groq,
}
VALID_MODELS: tuple[str, ...] = tuple(MODEL_SERVICE_MAP.keys())
SERVICE_APIKEY_ENVVAR_MAP: dict[EChatService, str] = {
    EChatService.Google: 'GOOGLE_API_KEY',
    EChatService.Groq: 'GROQ_API_KEY',
    EChatService.OpenAI: 'OPENAI_API_KEY',
}
