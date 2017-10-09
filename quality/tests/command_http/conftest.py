import pytest
from os.path import join
from test_lib.utils import copy_main_workspace
from restrek.core.context import RestrekContext
from restrek.core.services import PlanService
import restrek.constants as C


@pytest.fixture(scope='module')
def sch(tmpdir_factory):
    target_local_path = tmpdir_factory.mktemp('command_http')
    target_path = str(target_local_path)
    copy_main_workspace(target_path, 'command_http')
    ctx = RestrekContext(join(target_path, C.CMDS_DIR), join(target_path, C.PLANS_DIR), join(target_path, C.ENVIRONMENTS_DIR))
    return PlanService(ctx)
