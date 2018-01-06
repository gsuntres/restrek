import os
import ConfigParser

BOOL_TRUE_VARS = ['yes', 'true', 'on']


def load_config_file():
    ''' Load configuration file '''
    try:
        path0 = os.getcwd() + '/restrek.cfg'
    except OSError:
        path0 = None
    path1 = os.path.expanduser('~/.restrek.cfg')
    path2 = '/etc/restrek/restrek.cfg'

    for path in [path0, path1, path2]:
        if path is not None and os.path.exists(path):
            p = ConfigParser.RawConfigParser()
            p.read(path)
            return p, path

    return None, ''


def get_config(parser, section, key, default):
    value = default
    if parser is not None:
        try:
            value = parser.get(section, key)
        except:
            pass

    return value


def get_string(parser, section, key, default):
    val = get_config(parser, section, key, default)
    if val.startswith('"') and val.endswith('"'):
        val = val[1:-1]
    return val


def get_boolean(parser, section, key, default=False):
    val = get_config(parser, section, key, default)
    return val if isinstance(val, bool) else val in BOOL_TRUE_VARS

p, CONFIG_FILE_PATH = load_config_file()
DEFAULTS_KEY = 'defaults'

WS_DIR = get_string(p, DEFAULTS_KEY, 'workspace_dir', '.')

DEFAULT_CMDS_PATH = get_string(p, DEFAULTS_KEY, 'default_commands_dir', 'commands')
CONTINUE_ON_FAIL = get_boolean(p, DEFAULTS_KEY, 'continue_on_fail', False)
PRETTY_JSON = get_boolean(p, DEFAULTS_KEY, 'json_pretty', False)
PRINT_COLORS = get_boolean(p, DEFAULTS_KEY, 'print_colors', True)
PRINT_TIMESTAMP = get_boolean(p, DEFAULTS_KEY, 'print_timestamp', True)

RESERVED_WORDS = [
    'properties',
    'globals'
]

DEFAULT_ENV = 'devel'
PROPERTIES_NAME = 'properties'
GLOBALS_NAME = 'globals'
ENVIRONMENTS_NAME = 'envs'

CMDS_DIR = 'commands'
PLANS_DIR = 'plans'
VARS_DIR = 'vars'
ENVIRONMENTS_DIR = 'envs'

COMMAND_KEY = 'command'
PLAN_KEY = 'plan'
ENV_KEY = 'env'
TESTS_KEY = 'tests'
PAYLOAD_KEY = 'payload'
REGISTER_KEY = 'register'
PROPERTIES_KEY = 'properties'

INGNORED_EXTS = ('.pyc', '.swp', '.bak', '~', '.rpm', '.md', '.txt')
IGNORED_FILES = ('COPYING', 'CONTRIBUTING', 'LICENSE', 'README', 'VERSION', 'GUIDELINES')
FILENAME_REGEX = '^(\w+)(\.yaml|\.yml)?$'
GROUP_NAME_REGEG = '^\w+\.\w+$'
