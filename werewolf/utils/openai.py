from langchain_openai import ChatOpenAI
from ..const import DEFAULT_MODEL


def create_chat_openai_model(
    llm: ChatOpenAI | str | None = None,
) -> ChatOpenAI:
    """Create a ChatOpenAI instance.

    Args:
        llm (ChatOpenAI | str | None, optional): ChatOpenAI instance or model name. Defaults to None.

    Returns:
        ChatOpenAI: ChatOpenAI instance

    Note:

    """  # noqa
    if isinstance(llm, str):
        return ChatOpenAI(model=llm)
    else:
        return llm or ChatOpenAI(model=DEFAULT_MODEL)
