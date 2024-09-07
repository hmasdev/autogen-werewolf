import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import pytest
from pytest_mock import MockerFixture
from werewolf.const import DEFAULT_MODEL
from werewolf.utils.openai import create_chat_openai_model

load_dotenv()


def test_create_chat_openai_model_with_none(mocker: MockerFixture) -> None:  # noqa
    coai_mock = mocker.patch("werewolf.utils.openai.ChatOpenAI")
    create_chat_openai_model()  # type: ignore
    coai_mock.assert_called_once_with(model=DEFAULT_MODEL, seed=None)


@pytest.mark.parametrize("model_name", ["gpt-3.5-turbo", "gpt-4o-mini"])
def test_create_chat_openai_model_with_str(
    model_name: str,
    mocker: MockerFixture,
) -> None:
    coai_mock = mocker.patch("werewolf.utils.openai.ChatOpenAI")
    create_chat_openai_model(model_name)  # type: ignore
    coai_mock.assert_called_once_with(model=model_name, seed=None)


def test_create_chat_openai_model_with_instance(mocker: MockerFixture) -> None:  # noqa
    llm = mocker.MagicMock(spec=ChatOpenAI)
    actual: ChatOpenAI = create_chat_openai_model(llm)
    assert actual is llm


@pytest.mark.parametrize(
    'llm, seed',
    [
        ('gpt-3.5-turbo', 123),
        ('gpt-4o-mini', 456),
        ('gpt-4o-mini', None),
    ],
)
def test_create_chat_openai_model_return_same_instance_for_same_input(
    llm: str,
    seed: int,
    mocker: MockerFixture,
) -> None:
    ChatOpenAI_mock = mocker.patch(
        "werewolf.utils.openai.ChatOpenAI",
        return_value=mocker.MagicMock(spec=ChatOpenAI),
    )
    actual1: ChatOpenAI = create_chat_openai_model(llm, seed)  # type: ignore
    actual2: ChatOpenAI = create_chat_openai_model(llm, seed)  # type: ignore
    assert actual1 is actual2
    ChatOpenAI_mock.assert_called_once_with(model=llm, seed=seed)


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("OPENAI_API_KEY") is None,
    reason="OPENAI_API is not set.",
)
@pytest.mark.parametrize(
    'llm',
    [
        'gpt-3.5-turbo',
        None,
    ],
)
def test_create_chat_openai_model_with_real_instance(llm: str | None) -> None:
    actual: ChatOpenAI = create_chat_openai_model(llm)  # type: ignore
    assert isinstance(actual, ChatOpenAI)
