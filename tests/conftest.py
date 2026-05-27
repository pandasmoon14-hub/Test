import pytest

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8, registry_records_by_id


@pytest.fixture
def repo_root():
    return ROOT


@pytest.fixture
def registry_path():
    return REGISTRY_PATH


@pytest.fixture
def registry_records():
    return registry_records_by_id()


@pytest.fixture
def read_text():
    return read_utf8
