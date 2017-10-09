import sys
import os
import restrek.commands as empty
COMMAND_MODULES = []


def load_command_module(module_name):
    module_full_name = command_full_name(module_name)
    if module_name not in COMMAND_MODULES:
        try:
            __import__(module_full_name)
            COMMAND_MODULES.append(module_name)
        except ImportError as e:
            module_full_name = command_full_name('empty')
            try:
                __import__(module_full_name)
                COMMAND_MODULES.append(module_name)
            except ImportError as e:
                return None

    return sys.modules[module_full_name]


def command_full_name(name):
    return 'restrek.commands.%s' % name


def find_command_modules():
    cmd_modules = []
    for file in os.listdir(os.path.dirname(empty.__file__)):
        if is_python_source(file):
            cmd_modules.append(base(file))

    return cmd_modules


def base(file_name):
    return os.path.splitext(file_name)[0]


def is_python_source(name):
    return name and not name.startswith('_') and name.endswith('.py')
