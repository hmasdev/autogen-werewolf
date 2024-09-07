import os
from typing import Generator
from dotenv import load_dotenv
import pytest
from werewolf.const import SERVICE_APIKEY_ENVVAR_MAP


@pytest.fixture(scope='function')
def api_keys(dummy: str = 'dummy') -> Generator[None, None, None]:
    for envvar in SERVICE_APIKEY_ENVVAR_MAP.values():
        os.environ[envvar] = os.getenv(envvar) or dummy  # type: ignore
    load_dotenv()
    yield
    for envvar in SERVICE_APIKEY_ENVVAR_MAP.values():
        if os.getenv(envvar) == dummy:
            del os.environ[envvar]
