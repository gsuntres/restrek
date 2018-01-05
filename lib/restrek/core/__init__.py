import time
from restrek.errors import RestrekError, PlanError
from restrek.utils import split_name, combine_name, get_val, guid, now, props as utils_props, is_valid_identifier, arr_eq, isinstance_types
from restrek.utils.module_utils import load_command_module
import restrek.constants as C
from restrek.core.display import display

DEFAULT_KEY = 'default'

PROPS_SCHEMA = {
    'delay': {
        'desc': 'delay command execution (is seconds)',
        DEFAULT_KEY: 0
    },
    'debug': {
        'desc': 'enable debug',
        DEFAULT_KEY: False
    },
    'show_props': {
        'msg': 'Set to True to show command properties',
        DEFAULT_KEY: False
    }
}

# common properties among command modules
COMMON_PROPS = ['name', 'props', 'payload', 'schema_in', 'schema_out', 'results']

for k in PROPS_SCHEMA.keys():
    COMMON_PROPS.append(k)


class QualifierName(object):

    def __init__(self, group, name):
        self.group = group
        self.name = name

    @classmethod
    def from_string(cls, qname):
        group, name = split_name(qname.strip())
        return QualifierName(group, name)

    @property
    def qualifier(self):
        return combine_name(self.group, self.name)

    def __str__(self):
        return self.qualifier


class MetaCommand(type):

    def __init__(cls, name, base, clsdict):
        if 'run' in clsdict:
            def new_run(self):
                if self.delay and self.delay > 0:
                    time.sleep(self.delay)
                clsdict['run'](self)
            setattr(cls, 'run', new_run)


class SchemaException(RestrekError):

    def __init__(self, message=""):
        super(SchemaException, self).__init__(message)


class RestrekCommand(object):
    r""" Base abstract class to create commands.

    :param name: Command's terse description.
    :param props: (optional) Dictionary of properties that override input schema.
    :param payload: (optional) Dictionary with data to send.
    :param schema_in: Dictionary with the input schema
    :param schema_out: Dictionary with the output schema
    """

    __metaclass__ = MetaCommand

    def __init__(self, name='A terse description', props=dict(), payload=dict(), schema_in=dict(), schema_out=dict()):
        self.name = name
        self._props = props
        self.payload = payload
        self.schema_in = schema_in
        self.schema_in.update(PROPS_SCHEMA)
        self.schema_out = schema_out
        self._results = dict()
        self.parse()

    def run(self):
        raise NotImplementedError('Need to implement this')

    def parse(self):
        r"""Parse props and set attributes to the command according to its schema"""
        for k in self.schema_in:
            if k not in self._props:
                if DEFAULT_KEY in self.schema_in[k]:
                    setattr(self, k, self.schema_in[k][DEFAULT_KEY])
                else:
                    raise RestrekError('attribute `{}` in command `{}` is requried'.format(k, self.name))
            else:
                setattr(self, k, self._props[k])

    def parse_registration_statements(self, registration_statements):
        r"""Given a list of statements return the parsed env"""
        raise NotImplementedError('Need to implement this')

    @staticmethod
    def parse_registration_statement(target_kw, register_statement, context=dict()):
        r"""Will parse registration statement"""
        if not target_kw or not is_valid_identifier(target_kw):
            raise RestrekError('%s is not a valid keyword' % target_kw)

        out = dict()
        try:
            out[target_kw] = eval(register_statement, {}, context)
        except (NameError, KeyError, IndexError) as e:
            print 'Unknown element %s - %s' % (target_kw, e)
        except SyntaxError as e:
            print 'Invalid syntax %s' % e
        except TypeError as e:
            print 'Problem in statement `%s` (%r)' % (register_statement, e)

        return out

    @property
    def output(self):
        return get_val(self._results, 'output', dict())

    @output.setter
    def output(self, data):
        valid_data = self._ensure_schema_out(data)
        if self.show_props:
            display.supressed('[PROPERTIES]')
            display.supressed(self.props)
            valid_data['command_properties'] = self.props
        self._results['output'] = valid_data

    def _ensure_schema_out(self, data):
        if data is not None and isinstance(data, dict):
            if arr_eq(data.keys(), self.schema_out.keys()):
                return data
        raise SchemaException(message='data %r does not conform to output schema' % data)

    @property
    def unique_props(self):
        props = dict()
        for p in self.props:
            if p not in COMMON_PROPS:
                props[p] = self.__getattribute__(p)
        return props

    @property
    def props(self):
        props = dict()
        for p in utils_props(self):
            if p not in ['schema_in', 'schema_out']:
                val = self.__getattribute__(p)
                if isinstance_types(val, ['str', 'bool', 'int', 'float', 'long', 'dict']):
                    props[p] = val

        return props

    def log(self, msg):
        if self.debug:
            s = ''
            if isinstance_types(msg, ['str', 'unicode']):
                s = msg
            elif isinstance(msg, int):
                s = '%d' % msg
            else:
                s = '%s' % msg
            display.supressed(s)

    def __str__(self):
        return '[COMMAND]: %s' % self.name


class CommandDescription(object):

    def __init__(self, plugin, name, props):
        self.plugin = plugin
        self.name = name
        self.props = props

    @classmethod
    def from_raw(cls, data):
        cmd_attrs = data.keys()

        descr = data[cmd_attrs.pop(cmd_attrs.index('name'))] if 'name' in cmd_attrs else None

        if len(cmd_attrs) > 1:
            raise RestrekError('malformed plan')

        if len(cmd_attrs) == 0:
            raise RestrekError('plan is missing a plugin to run')

        plugin_name = cmd_attrs.pop(0)
        props = data[plugin_name]

        return cls(plugin_name, descr, props)

    def __str__(self):
        return 'name: %s \nplugin: %s \nprops: %s' % (self.name, self.plugin, self.props)


class Plan(object):

    def __init__(self, obj, qname):
        self.qname = qname
        self.steps = []
        if isinstance(obj, list):
            self.steps = obj

    def __getitem__(self, index):
        step_obj = self.steps[index]
        return self.steps[index]

    def __str__(self):
        return 'Plan [%s] steps: %s' % (self.qname.qualifier, str(len(self.steps)))


class ExecutionInfo:

    def __init__(self):
        self.started = now()
        self.finished = None
        self.test_num_succeeded = 0
        self.test_num_failed = 0

    @property
    def duration(self):
        if not self.finished:
            self.finished = now()
        d = self.finished - self.started
        return d.microseconds / 1000


class StepSession(object):

    def __init__(self, step, command=None):
        self.id = guid()
        self.step = step
        self.command = command
        self._runnable_command = None
        self.info = ExecutionInfo()
        self._registered = {}

    def commit(self):
        if self.runnable_command:
            self.runnable_command.run()

    @property
    def runnable_command(self):
        if self._runnable_command is None and self.command:
            runnable_command_module = load_command_module(self.command.plugin)
            self._runnable_command = runnable_command_module.command(self.command.name, self.command.props, self.payload)
        return self._runnable_command

    @property
    def name(self):
        s = '[-]'
        if self.command:
            s = '[%s]' % self.command.plugin
        s += ' %s' % get_val(self.step, C.COMMAND_KEY, '----')
        return s

    @property
    def tests(self):
        return get_val(self.step, C.TESTS_KEY)

    @property
    def payload(self):
        return get_val(self.step, C.PAYLOAD_KEY)

    @property
    def properties(self):
        return get_val(self.step, C.PROPERTIES_KEY)

    @property
    def duration(self):
        return self.info.duration

    @property
    def output(self):
        out = dict(duration=self.info.duration)
        if self.runnable_command:
            out.update(self.runnable_command.output)
        return out

    @property
    def skip(self):
        return self.step['skip'] if 'skip' in self.step else False

    @property
    def register(self):
        return self.step[C.REGISTER_KEY] if C.REGISTER_KEY in self.step else None

    @property
    def registered(self):
        if not self._registered:
            if self.register:
                if self.runnable_command:
                    self._registered = self.runnable_command.parse_registration_statements(self.register)
                else:
                    self._registered = self.register

        return self._registered

    def __str__(self):
        s = '[%s]\n' % self.id
        s += '[STEP]\n%s' % self.step
        if self.command:
            s += '\n[COMMAND]\n%s' % self.command
        return s
