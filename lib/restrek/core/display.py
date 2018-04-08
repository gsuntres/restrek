# -*- coding: utf-8 -*-
import pprint
import restrek.utils as utils
import restrek.constants as C


MAX_TEXT_LENGTH = 1000
PRETTY_INDENT = 2


class Colors:
    MAGENTA = 'magenta'
    BMAGENTA = 'bmagenta'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    RED = 'red'
    GRAY = 'gray'

    def __init__(self):
        self._colors = {
            'magenta': '\033[95m',
            'bmagenta': '\033[1;95m',
            'blue': '\033[94m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'gray': '\033[1;30m'
        }
        self.ENDC = '\033[0m'

    def get_color(self, color):
        return self._colors[color] if self.has_color(color) else self.ENDC

    def has_color(self, color):
        return color and color in self.colors

    @property
    def endc(self):
        return self.ENDC

    @property
    def colors(self):
        return self._colors.keys()


class Display(object):

    def __init__(self, with_colors, with_timestamp):
        self.pp = pprint.PrettyPrinter(indent=PRETTY_INDENT)
        self.with_colors = with_colors
        self.with_timestamp = with_timestamp
        self.c = Colors()

    def log(self, msg):
        self._log(msg, None)

    def success(self, msg):
        self._log(msg, 'green')

    def err(self, msg):
        self._log(msg, 'red')

    def warn(self, msg):
        self._log(msg, 'yellow')

    def title_big(self, msg):
        self._log(msg, 'bmagenta')

    def title(self, msg):
        self._log(msg, 'magenta')

    def supressed(self, msg):
        self._log(msg, 'gray')

    def _log(self, msg, color):
        if utils.isinstance_types(msg, ['dict', 'list']):
            msg = self.pp.pformat(msg)

        # truncate
        if utils.isinstance_types(msg, ['str', 'unicode']) and len(msg) > MAX_TEXT_LENGTH:
            msg = (msg[:MAX_TEXT_LENGTH] + '..')

        if self.c.has_color(color) and self.with_colors:
            msg = '{}{}{}'.format(self.c.get_color(color), msg, self.c.endc)
        else:
            msg = '{}'.format(msg)

        if self.with_timestamp:
            msg = '[{}] {}'.format(utils.now_str(), msg)

        print msg


display = Display(C.PRINT_COLORS, C.PRINT_TIMESTAMP)
