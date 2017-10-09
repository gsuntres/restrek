import os
import ConfigParser
import restrek.constants as C
from restrek.errors import RestrekError
from restrek.core.context import RestrekContext
from restrek.core.services import PlanService
from restrek.utils import trim_all

RUN_SECTION = 'run'
ALL = 'all'
PLANS_KEY = 'plans'
IGNORE_KEY = 'ignore'


class BaseRunner(object):
    r"""Will run all plans or take isntructions on how to do that from a `Trekfile`"""

    def __init__(self, workspace=C.WS_DIR, env=C.DEFAULT_ENV, verbose=None):
        self.ctx = RestrekContext(workspace, env, verbose)
        self.plans_hdl = PlanService(self.ctx)
        self.parser, _ = load_config_file(workspace)
        self.plans_to_run = []

        self._prepare_plans()

        self.run()

    def _get_opt(self, section, key, default=None):
        v = default
        try:
            v = self.parser.get(section, key)
        except ConfigParser.NoOptionError as e:
            pass
        return v

    def _get_str(self, section, key, default=''):
        return self._get_opt(section, key, default)

    def _prepare_plans(self):
        all_plans = self.ctx.get_plans()
        requested_plans = trim_all(self._get_str(RUN_SECTION, PLANS_KEY)).split(',')
        ignore_plans = trim_all(self._get_str(RUN_SECTION, IGNORE_KEY)).split(',')

        should_run_all = False
        if ALL in requested_plans:
            should_run_all = True
            del requested_plans[requested_plans.index(ALL)]

        if len(requested_plans) == 1 and not requested_plans[0]:
            raise RestrekError('No plans specified')

        for p in requested_plans:
            if p not in all_plans:
                raise RestrekError('Unknown plan %s' % p)

        all_plans_but_requested = [x for x in all_plans if x not in requested_plans]

        _plans = requested_plans
        if should_run_all:
            _plans.extend(all_plans_but_requested)

        self.plans_to_run = [x for x in _plans if x not in ignore_plans]

    def run(self):
        self.plans_hdl.execute_multiple_plans(self.plans_to_run)


def load_config_file(workspace):
    ''' Load configuration file '''
    try:
        path = os.path.join(workspace, 'Trekfile')
    except OSError:
        path = None

    if path is not None and os.path.exists(path):
            p = ConfigParser.RawConfigParser()
            p.read(path)
            return p, path

    return None, ''
