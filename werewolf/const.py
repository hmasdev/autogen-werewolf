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
    VillagersWinCondition = 'All werewolves are excluded from the game'
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
    # ref. https://platform.openai.com/docs/pricing
    'gpt-4o': EChatService.OpenAI,
    'gpt-4o-mini': EChatService.OpenAI,
    'o1': EChatService.OpenAI,  # NOTE: it may be too expensive # TODO: fix a problem that logs like `params={'messages': ...` are displayed  # noqa: E501
    'o3-mini': EChatService.OpenAI,  # TODO: fix a problem that 'WARNING:autogen.oai.client:Model o3-mini-2025-01-31 is not found.' is displayed  # noqa: E501
    'o1-mini': EChatService.OpenAI,  # TODO: fix a problem that logs like `params={'messages': ...` are displayed  # noqa: E501
    'gpt-3.5-turbo': EChatService.OpenAI,
    'gpt-4': EChatService.OpenAI,
    'gpt-4-turbo': EChatService.OpenAI,
    # ref. https://ai.google.dev/gemini-api/docs/models
    # 'gemini-2.5-pro-preview-03-25': EChatService.Google,
    'gemini-2.0-flash': EChatService.Google,
    'gemini-2.0-flash-lite': EChatService.Google,
    'gemini-1.5-flash': EChatService.Google,
    'gemini-1.5-flash-8b': EChatService.Google,
    'gemini-1.5-pro': EChatService.Google,
    # TODO: add gemma series
    # ref. https://groq.com/pricing/
    'qwen-2.5-32b': EChatService.Groq,
    'qwen-2.5-coder-32b': EChatService.Groq,
    'qwen-qwq-32b': EChatService.Groq,
    'deepseek-r1-distill-qwen-32b': EChatService.Groq,
    'deepseek-r1-distill-llama-70b': EChatService.Groq,
    'gemma2-9b-it': EChatService.Groq,  # TODO: the name is too similar to Google's one.  # noqa: E501
    'llama-3.1-8b-instant': EChatService.Groq,
    'llama-3.2-1b-preview': EChatService.Groq,
    'llama-3.2-3b-preview': EChatService.Groq,
    'llama-3.3-70b-specdec': EChatService.Groq,
    'llama-3.3-70b-versatile': EChatService.Groq,
    'llama3-70b-8192': EChatService.Groq,
    'llama3-8b-8192': EChatService.Groq,
    'meta-llama/llama-4-maverick-17b-128e-instruct': EChatService.Groq,
    'meta-llama/llama-4-scout-17b-16e-instruct': EChatService.Groq,
    'mistral-saba-24b': EChatService.Groq,
}
VALID_MODELS: tuple[str, ...] = tuple(MODEL_SERVICE_MAP.keys())
SERVICE_APIKEY_ENVVAR_MAP: dict[EChatService, str] = {
    EChatService.Google: 'GOOGLE_API_KEY',
    EChatService.Groq: 'GROQ_API_KEY',
    EChatService.OpenAI: 'OPENAI_API_KEY',
}
