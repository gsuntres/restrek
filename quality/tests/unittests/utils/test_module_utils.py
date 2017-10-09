import pytest
import restrek.utils.module_utils as utils
from restrek.commands.empty import EmptyCommand
from restrek.commands.http import HttpCommand


def test_on_unknown_command_should_return_empty_command():
    mod = utils.load_command_module('barboutsala')
    assert mod.command == EmptyCommand


def test_load_existing_command():
    mod = utils.load_command_module('http')
    assert mod.command == HttpCommand
