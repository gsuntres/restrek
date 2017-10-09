from restrek.core import RestrekCommand, DEFAULT_KEY

SCHEMA_IN = {
    'msg': {
        'msg': 'message to echo',
        DEFAULT_KEY: ''
    }
}

SCHEMA_OUT = {
    'msg': 'The echoed message or a list of properties'
}


class EchoCommand(RestrekCommand):

    def __init__(self, name, props, payload):
        RestrekCommand.__init__(self, name, props, payload, SCHEMA_IN, SCHEMA_OUT)

    def run(self):
        self.log(self.msg)
        self.output = dict(msg=self.msg)

    def parse_registration_statements(self, register_statements):
        return register_statements

command = EchoCommand
