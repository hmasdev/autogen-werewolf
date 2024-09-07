from functools import lru_cache
from logging import getLogger, Logger
from langchain_core.language_models import BaseChatModel
# from langchain_community.chat_models import ChatPerplexity
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from .const import DEFAULT_MODEL, EChatService, MODEL_SERVICE_MAP


_service2cls: dict[EChatService, type[BaseChatModel]] = {
    EChatService.OpenAI: ChatOpenAI,
    EChatService.Google: ChatGoogleGenerativeAI,
    EChatService.Groq: ChatGroq,
}


@lru_cache(maxsize=None)
def create_chat_model(
    llm: BaseChatModel | str = DEFAULT_MODEL,
    seed: int | None = None,
    logger: Logger = getLogger(__name__),
    **kwargs,
) -> BaseChatModel:
    """Create a ChatModel instance.

    Args:
        llm (BaseChatModel | str, optional): ChatModel instance or model name. Defaults to DEFAULT_MODEL.
        seed (int, optional): Random seed. Defaults to None.
        logger (Logger, optional): Logger. Defaults to getLogger(__name__).

    Raises:
        ValueError: Unknown model name

    Returns:
        BaseChatModel: ChatModel instance

    Note:
        seed is used only when llm is a str.
        The same parameters return the same instance.
    """  # noqa
    llm = llm or DEFAULT_MODEL
    if isinstance(llm, str):
        try:
            if seed is not None:
                return _service2cls[MODEL_SERVICE_MAP[llm]](model=llm, seed=seed, **kwargs)  # type: ignore  # noqa
            else:
                return _service2cls[MODEL_SERVICE_MAP[llm]](model=llm, **kwargs)  # type: ignore  # noqa
        except TypeError:
            logger.warning(f'{llm} does not support seed.')
            return _service2cls[MODEL_SERVICE_MAP[llm]](model=llm, **kwargs)  # type: ignore  # noqa
        except KeyError:
            raise ValueError(f'Unknown model name: {llm}')
    else:
        return llm
