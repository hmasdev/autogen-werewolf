import os
from dotenv import load_dotenv
import pytest
from werewolf.const import SERVICE_APIKEY_ENVVAR_MAP


@pytest.fixture(scope='session', autouse=True)
def api_keys():
    for envvar in SERVICE_APIKEY_ENVVAR_MAP.values():
        os.environ[envvar] = os.getenv(envvar) or ''  # type: ignore
    load_dotenv()
    yield
