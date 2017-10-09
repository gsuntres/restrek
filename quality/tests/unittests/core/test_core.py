import pytest
from restrek.core import SchemaException, RestrekCommand, StepSession, QualifierName
from restrek.errors import RestrekError

SCHEMA_IN = {
    'prop1': {
        'desc': 'prop1 desciption',
        'default': 10
    },
    'prop2_required': {
        'desc': 'prop2 desciption is required'
    }
}

SCHEMA_OUT = {
    'out1': 'out1 value returned',
    'out2': 'out2 value returned'
}

# TEST COMMANDS #


class WithRequiredPropCommand(RestrekCommand):

    def __init__(self, name='mocked command', props=dict(), payload=dict()):
        RestrekCommand.__init__(self, name, props, payload, SCHEMA_IN, SCHEMA_OUT)


def test_base_command(command):
    assert 'mycommand554' == command.name
    assert dict(foo='bar') == command.payload


def test_required_property():
    with pytest.raises(RestrekError) as e:
        WithRequiredPropCommand()
    assert 'prop2_required' in e.value.message


def test_command_run_should_be_abstract(command):
    with pytest.raises(NotImplementedError):
        command.run()


def test_props(mocked):
    props = mocked.props
    uprops = mocked.unique_props.keys()
    ps = set(props).intersection(set(uprops))
    print uprops
    assert 5 == len(ps)
    assert 'prop1' in ps
    assert 'prop2' in ps
    assert 'prop3' in ps
    assert 'prop4' in ps
    assert 'prop5_required' in ps


def test_ensure_schema_out_incompatible_data(mocked):
    data = {'out1': 'this is ok', 'out22': 'this is not ok'}

    with pytest.raises(SchemaException):
        mocked._ensure_schema_out(data)


def test_ensure_schema_out(mocked):
    data = {'out1': 'this is ok', 'out2': 'this is not ok'}
    mocked._ensure_schema_out(data)


def test_parse_registration_statement(command):
    ctx = {'var1': {'k1': 'thisisval1', 'k2': 'thisisval2'}}
    r = RestrekCommand.parse_registration_statement('key1', 'var1[\'k2\']', ctx)
    assert {'key1': 'thisisval2'} == r


def test_parse_registration_statement_unicode(command):
    ctx = {u'var1': {u'k1': u'thisisval1', u'k2': u'thisisval2'}}
    r = RestrekCommand.parse_registration_statement('key1', 'var1[\'k2\']', ctx)
    assert {'key1': 'thisisval2'} == r


# Test Step Session #
def test_step_session_returns_register_as_vars(step_nocmd):
    sess = StepSession(step_nocmd)
    assert {'var1': 'out1', 'var2': 'out2'} == sess.registered


# Misc #

def test_qualifier_name():
    q = QualifierName.from_string('group100.name200')
    assert 'group100' == q.group
    assert 'name200' == q.name
    assert 'group100.name200' == q.qualifier


def test_qualifier_name_trim():
    q = QualifierName.from_string('       group100.name200  ')
    assert 'group100' == q.group
    assert 'name200' == q.name
    assert 'group100.name200' == q.qualifier
