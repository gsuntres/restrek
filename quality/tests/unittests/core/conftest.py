import pytest
from restrek.core.context import VarsManager
from restrek.core import RestrekCommand, CommandDescription

SCHEMA_IN = {
    'prop1': {
        'desc': 'prop1 description is of type string(unicode)',
        'default': 'strval'
    },
    'prop2': {
        'desc': 'prop2 description is of type int',
        'default': 100
    },
    'prop3': {
        'desc': 'prop3 description is of type dict',
        'default': dict()
    },
    'prop4': {
        'desc': 'prop4 desciption is of type float',
        'default': 0.123
    },
    'prop5_required': {
        'desc': 'prop5 desciption is required'
    }

}

SCHEMA_OUT = {
    'out1': 'out1 value returned',
    'out2': 'out2 value returned'
}


class MockedCommand(RestrekCommand):

    def __init__(self, name='mocked command', props=dict(), payload=dict()):
        RestrekCommand.__init__(self, name, props, payload, SCHEMA_IN, SCHEMA_OUT)


@pytest.fixture(scope='session')
def mocked():
    props = {
        'prop2': 200,
        'prop5_required': 'foo'
    }
    payload = {
        'foo': 'bar'
    }
    return MockedCommand(name='my mocked command', props=props, payload=payload)


@pytest.fixture(scope='module')
def command():
    return RestrekCommand('mycommand554', dict(host='www.bla.gr', secure=True), dict(foo='bar'))

COMMAND_DESCR = {
    'name': 'A command description',
    'http': {
        'prop1': 200,
        'prop2': 'a simple lonely prop'
    }
}


@pytest.fixture(scope='module')
def command_descr():
    return CommandDescription.from_raw(COMMAND_DESCR)

STEP = {
    'data': {'foo': 'bar'},
    'register': {
        'var1': 'out1',
        'var2': 'out2'
    },
    'tests': {
        'This is my assert': 'out1 is None'
    }
}


@pytest.fixture(scope='session')
def step_nocmd():
    return STEP


@pytest.fixture(scope='session')
def vars_mgr():
    return VarsManager()
