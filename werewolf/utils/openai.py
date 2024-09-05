from functools import lru_cache
from langchain_openai import ChatOpenAI
from ..const import DEFAULT_MODEL


@lru_cache(maxsize=None)
def create_chat_openai_model(
    llm: ChatOpenAI | str | None = None,
    seed: int | None = None,
) -> ChatOpenAI:
    """Create a ChatOpenAI instance.

    Args:
        llm (ChatOpenAI | str | None, optional): ChatOpenAI instance or model name. Defaults to None.
        seed (int, optional): Random seed. Defaults to None.

    Returns:
        ChatOpenAI: ChatOpenAI instance

    Note:
        seed is used only when llm is a str or None.
    """  # noqa
    if isinstance(llm, str):
        return ChatOpenAI(model=llm, seed=seed)
    else:
        return llm or ChatOpenAI(model=DEFAULT_MODEL, seed=seed)
