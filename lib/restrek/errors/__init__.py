class RestrekError(Exception):
    """
    Usage:

        raise RestrekError('some message here')
    """

    def __init__(self, message=""):
        self.message = message

    def __str__(self):
        return 'Error: %s' % self.message

    def __repr__(self):
        return self.message


class UnknownElementError(RestrekError):
    ''' unknown element in plan, command or details file '''
    pass


class PlanError(RestrekError):
    pass


class RestrekOptionsError(RestrekError):
    ''' bad or incomplete options passed '''
    pass
