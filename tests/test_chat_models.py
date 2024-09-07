import os
from dotenv import load_dotenv
import pytest
from pytest_mock import MockerFixture
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from werewolf.chat_models import create_chat_model, _service2cls
from werewolf.const import MODEL_SERVICE_MAP

load_dotenv()

name2cls: dict[str, type[BaseChatModel]] = {
    k: _service2cls[v]
    for k, v in MODEL_SERVICE_MAP.items()
}


@pytest.mark.parametrize(
    'llm, expected',
    [(k, v) for _, (k, v) in enumerate(name2cls.items())]
)
def test_create_chat_model_wo_seed(
    llm: str,
    expected: type[BaseChatModel],
    mocker: MockerFixture,
) -> None:
    mocker.patch(f'werewolf.chat_models.{expected.__name__}', autospec=True)  # noqa
    assert isinstance(create_chat_model(llm), expected)


@pytest.mark.parametrize(
    'llm, seed, expected',
    [(k, i, v) for i, (k, v) in enumerate(name2cls.items())]
)
def test_create_chat_model_w_seed(
    llm: str,
    seed: int,
    expected: type[BaseChatModel],
    mocker: MockerFixture,
) -> None:
    cls_mock = mocker.patch(f'werewolf.chat_models.{expected.__name__}', autospec=True)  # noqa
    assert isinstance(create_chat_model(llm, seed), expected)

    # TODO: fix the following assertion
    # cls_mock.assert_called_once_with(model=llm, seed=seed)


def test_create_chat_model_w_invalid_llm() -> None:
    with pytest.raises(ValueError):
        create_chat_model('invalid')


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("OPENAI_API_KEY") is None,
    reason="OPENAI_API is not set.",
)
@pytest.mark.parametrize(
    'llm',
    [
        'gpt-4o-mini',
        'gpt-4',
        'gpt-4-turbo',
        'gpt-4o',
        'gpt-3.5-turbo',
    ]
)
def test_create_chat_model_for_ChatOpenAI_integration(llm: str) -> None:
    assert isinstance(create_chat_model(llm), ChatOpenAI)


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("GROQ_API_KEY") is None,
    reason="GROQ_API_KEY is not set.",
)
@pytest.mark.parametrize(
    'llm',
    [
        'llama3-groq-70b-8192-tool-use-preview',
        'llama3-groq-8b-8192-tool-use-preview',
        'llama-3.1-70b-versatile',
        'llama-3.1-8b-instant',
        'llama-guard-3-8b',
        'llava-v1.5-7b-4096-preview',
        'llama3-70b-8192',
        'llama3-8b-8192',
        'mixtral-8x7b-32768',
        'gemma2-9b-it',
        'gemma2-7b-it',
    ]
)
def test_create_chat_model_for_ChatGroq_integration(llm: str) -> None:
    assert isinstance(create_chat_model(llm), ChatGroq)


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("GOOGLE_API_KEY") is None,
    reason="GOOGLE_API_KEY is not set.",
)
@pytest.mark.parametrize(
    'llm',
    [
        'gemini-1.5-flash',
        'gemini-pro-vision',
        'gemini-pro',
    ]
)
def test_create_chat_model_for_ChatGoogleGenerativeAI_integration(llm: str) -> None:  # noqa
    assert isinstance(create_chat_model(llm), ChatGoogleGenerativeAI)
