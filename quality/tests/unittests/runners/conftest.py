import pytest
from mock import Mock
from restrek.runners.base_runner import BaseRunner

# mock _prepare_plans since there is no Trekfile to load
BaseRunner._prepare_plans = Mock(return_value=None)


@pytest.fixture(scope='module')
def runner(ctx_ws):
    return BaseRunner(workspace=ctx_ws)
