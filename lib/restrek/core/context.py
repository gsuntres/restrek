import os
from os.path import isfile, join
import restrek.constants as C
import restrek.utils as utils
from restrek.utils.module_utils import find_command_modules
from restrek.parsing import yaml_load
from restrek.parsing.dataloader import DataLoader
from restrek.core import QualifierName
from restrek.core.workspace import FileWorkspaceManager
from restrek.core.display import display


class VarsManager(object):

    def __init__(self):
        self._registered = dict()

    def update(self, v):
        if v is not None and isinstance(v, dict):
            # if v and isinstance(v, dict):
            #     self._registered = deep_update(self._registered, v)
            # self._registered = merge(self._registered, v)
            self._registered.update(v)
        # self._registered = v

    @property
    def registered(self):
        return self._registered


class RestrekContext:

    def __init__(self, commands_dir, plans_dir, environments_dir, env=C.DEFAULT_ENV, verbose=None):
        self.env = env
        self.verbose = verbose
        self.ws_manager = FileWorkspaceManager(commands_dir, plans_dir, environments_dir, env)
        self.loader = DataLoader(commands_dir, plans_dir)
        self.vars_mgr = VarsManager()
        self.load()

    def load(self):
        self._parse_vars(self.env)

    def reload(self):
        self.load()
        self.ws_manager.reload()

    def get_plans(self, group=None):
        return self.ws_manager.get_plans(group)

    def get_commands(self, group=None):
        return self.ws_manager.get_commands(group)

    def get_command_groups(self):
        return self.ws_manager.get_command_groups()

    def get_plan_groups(self):
        return self.ws_manager.get_plan_groups()

    def load_plan(self, qualifier):
        return self.loader.load_plan(qualifier)

    def load_step(self, step_source):
        return self.loader.load_step(step_source, self.vars_mgr.registered)

    def load_cmd(self, qualifier):
        return self.loader.load_cmd(qualifier, self.vars_mgr.registered)

    def add_to_vars(self, data=dict()):
        self.vars_mgr.update(data)

    def log(self, msg):
        display.log(msg)

    @property
    def registered(self):
        return self.vars_mgr.registered

    def _parse_vars(self, env=C.DEFAULT_ENV):
        for file in self.ws_manager.vars_source:
            with open(file, 'r') as f:
                obj = yaml_load(f)
                if obj:
                    self.vars_mgr.update(obj)

    def merge_properties(self, command, plan_group=C.GLOBALS_NAME, command_group=None):
        plugin = command.plugin if hasattr(command, 'plugin') else None
        properties = self._get_default_properties(plugin)
        possible_properties = self._get_properties(plan_group, command_group, plugin)
        if possible_properties:
            properties.update(possible_properties)
        properties.update(command.props)
        c = utils.clone(command)
        c.props = properties
        return c

    def compact_properties(self, properties, plugin=None):
        possible_properties = properties.pop(self.env, False)
        if possible_properties:
            properties.update(possible_properties)
        if plugin is not None and plugin in find_command_modules():
            possible_properties = properties.pop(plugin, False)
            if possible_properties:
                properties.update(possible_properties)

        # when verbose set debug to true no matter what!
        if self.verbose:
            properties['debug'] = True

        return properties

    def _get_default_properties(self, plugin):
        props = dict()
        props_source = self.ws_manager.get_env_properties_source()
        props = self.loader.load_properties(props_source, self.vars_mgr.registered)
        return self.compact_properties(props, plugin)

    def _get_properties(self, plan_group, command_group, plugin):
        properties = self._get_properties_from_plans(plan_group, plugin)
        if command_group is not None:
            d = self._get_properties_from_commands(command_group, plugin)
            properties.update(d)
        return properties

    def _get_properties_from_commands(self, group, plugin):
        props = dict()
        props_source = self.ws_manager.get_command_properties_source(group)
        if props_source:
            props = self.loader.load_properties(props_source, self.vars_mgr.registered)
        return self.compact_properties(props, plugin)

    def _get_properties_from_plans(self, group, plugin):
        props = dict()
        props_source = self.ws_manager.get_plan_properties_source(group)
        if props_source:
            props = self.loader.load_properties(props_source, self.vars_mgr.registered)
        return self.compact_properties(props, plugin)
