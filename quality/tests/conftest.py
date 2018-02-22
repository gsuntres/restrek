import pytest
import restrek.constants as C
from os.path import join
from test_lib.utils import copy_main_workspace
from restrek.core.context import RestrekContext
from restrek.core.services import PlanService
from restrek.parsing.dataloader import DataLoader
from restrek.errors import RestrekError


@pytest.fixture(scope='module')
def ctx(tmpdir_factory):
    target_local_path = tmpdir_factory.mktemp('test_context')
    target_path = str(target_local_path)
    copy_main_workspace(target_path)
    return RestrekContext(join(target_path, C.CMDS_DIR), join(target_path, C.PLANS_DIR), join(target_path, C.ENVIRONMENTS_DIR))


@pytest.fixture(scope='module')
def ctx_ws(tmpdir_factory):
    target_local_path = tmpdir_factory.mktemp('test_context_ws')
    target_path = str(target_local_path)
    copy_main_workspace(target_path)
    return target_path


@pytest.fixture(scope='module')
def ctx_with_global_properties(tmpdir_factory):
    target_local_path = tmpdir_factory.mktemp('test_context_with_global_properties')
    target_path = str(target_local_path)
    copy_main_workspace(target_path, 'with_global_properties')
    return RestrekContext(join(target_path, C.CMDS_DIR), join(target_path, C.PLANS_DIR), join(target_path, C.ENVIRONMENTS_DIR))


@pytest.fixture(scope='module')
def ctx_no_global_properties(tmpdir_factory):
    target_local_path = tmpdir_factory.mktemp('test_context_no_global_properties')
    target_path = str(target_local_path)
    copy_main_workspace(target_path, 'with_global_properties')
    return RestrekContext(join(target_path, C.CMDS_DIR), join(target_path, C.PLANS_DIR), join(target_path, C.ENVIRONMENTS_DIR))


@pytest.fixture(scope='module')
def dataloader(tmpdir_factory):
    target_local_path = tmpdir_factory.mktemp('test_dataloader')
    target_path = str(target_local_path)
    copy_main_workspace(target_path)
    return DataLoader(join(target_path, C.CMDS_DIR), join(target_path, C.PLANS_DIR))


@pytest.fixture(scope='module')
def scheduler(tmpdir_factory):
    target_local_path = tmpdir_factory.mktemp('test_services')
    target_path = str(target_local_path)
    copy_main_workspace(target_path)
    ctx = RestrekContext(join(target_path, C.CMDS_DIR), join(target_path, C.PLANS_DIR), join(target_path, C.ENVIRONMENTS_DIR))
    return PlanService(ctx)
