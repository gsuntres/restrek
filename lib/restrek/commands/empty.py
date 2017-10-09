from restrek.core import RestrekCommand


class EmptyCommand(RestrekCommand):

    def __init__(self):
        super(RestrekCommand, self).__init__(name='Dummy Command')

    def run(self):
        pass

    def parse_registration_statements(self, register_statements):
        return register_statements

command = EmptyCommand
