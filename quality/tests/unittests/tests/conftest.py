import pytest
from restrek.tests import TestsManager


@pytest.fixture(scope='session')
def tests_mgr():
    return TestsManager()
