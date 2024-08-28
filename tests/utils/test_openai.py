import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import pytest
from pytest_mock import MockerFixture
from werewolf.const import DEFAULT_MODEL
from werewolf.utils.openai import create_chat_openai_model

load_dotenv()


def test_create_chat_openai_model_with_none(mocker: MockerFixture):
    coai_mock = mocker.patch("werewolf.utils.openai.ChatOpenAI")
    create_chat_openai_model()
    coai_mock.assert_called_once_with(model=DEFAULT_MODEL)


@pytest.mark.parametrize("model_name", ["gpt-3.5-turbo", "gpt-4o-mini"])
def test_create_chat_openai_model_with_str(
    model_name: str,
    mocker: MockerFixture,
):
    coai_mock = mocker.patch("werewolf.utils.openai.ChatOpenAI")
    create_chat_openai_model(model_name)
    coai_mock.assert_called_once_with(model=model_name)


def test_create_chat_openai_model_with_instance(mocker: MockerFixture):
    llm = mocker.MagicMock(spec=ChatOpenAI)
    actual = create_chat_openai_model(llm)
    assert actual is llm


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
def test_create_chat_openai_model_with_real_instance(llm: str | None):
    actual = create_chat_openai_model(llm)
    assert isinstance(actual, ChatOpenAI)
