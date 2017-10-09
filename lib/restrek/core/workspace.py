# -*- coding: utf-8 -*-

import os
from os.path import join, isdir, isfile, splitext
import restrek.constants as C
import restrek.utils as utils


class WorkspaceManager(object):
    r"""Holds infromation about the location of plans and commands.

        A typical structure might be:
        .
        ├── commands
        │   └── misc
        │       ├── get_account
        │       └── login
        ├── plans
        │   ├── properties
        │   └── misc
        │       ├── get_account
        │       └── login
        └── envs
            └── devel
                ├── properties
                └── vars
                    └── common
    """

    def get_plans(self, group=None):
        r"""Return a list of plans, if a group is provided filter accordingly"""
        raise NotImplementedError('Need to implement this')

    def get_commands(self, group=None):
        raise NotImplementedError('Need to implement this')

    def get_command_groups(self):
        raise NotImplementedError('Need to implement this')

    def get_plan_groups(self):
        raise NotImplementedError('Need to implement this')

    def group_has_details(self):
        raise NotImplementedError('Need to implement this')

    def get_command_properties_source(self):
        r"""Get environment details"""
        raise NotImplementedError('Need to implement this')

    def get_plan_properties_source(self, group=None):
        r"""Get details source for a group, if there is none return the global"""
        raise NotImplementedError('Need to implement this')

    @property
    def vars_source(self):
        r"""Return a list of files with variables"""
        raise NotImplementedError('Need to implement this')


class FileWorkspaceManager(WorkspaceManager):

    def __init__(self,
                 commands_dir,
                 plans_dir,
                 environments_dir,
                 env=C.DEFAULT_ENV):
        self.env = env
        self.commands_dir = commands_dir
        self.plans_dir = plans_dir
        self.environments_dir = environments_dir
        self._vars_source = dict()
        self.plan_groups = dict()
        self.plans_by_group = dict()
        self.command_groups = dict()
        self.commands_by_group = dict()
        self.properties_source = {
            C.COMMAND_KEY: {},
            C.PLAN_KEY: {}
        }
        self.plans_source = dict()
        self._load()

    def reload(self):
        self._load()

    def get_plans(self, group=None):
        if group in self.plans_by_group:
            return self.plans_by_group[group]
        else:
            plans = []
            for g in self.get_plan_groups():
                for p in self.plans_by_group[g]:
                    plans.append(utils.combine_name(g, utils.strip_ext(p)))
            return plans

    def get_commands(self, group=None):
        if group in self.commands_by_group:
            return self.commands_by_group[group]
        else:
            commands = []
            for g in self.get_command_groups():
                for cmd in self.commands_by_group[g]:
                    commands.append(utils.combine_name(g, cmd))
            return commands

    def get_command_groups(self):
        return self.command_groups.keys()

    def get_plan_groups(self):
        return self.plan_groups.keys()

    def get_command_properties_source(self, group=None):
        if group not in self.properties_source[C.COMMAND_KEY]:
            group = C.GLOBALS_NAME
        return self.properties_source[C.COMMAND_KEY][group] if group in self.properties_source[C.COMMAND_KEY] else None

    def get_plan_properties_source(self, group=None):
        if group not in self.properties_source[C.PLAN_KEY]:
            group = C.GLOBALS_NAME

        return self.properties_source[C.PLAN_KEY][group] if group in self.properties_source[C.PLAN_KEY] else None

    @property
    def vars_source(self):
        return self._vars_source.values()

    def _load(self):
        self._load_groups_commands()
        self._load_groups_plans()
        self._load_vars()

    def _load_groups_commands(self):
        self.command_groups = dict()
        self.commands_by_group = dict()
        self._load_properties_from_commands(self.commands_dir)
        for g in os.listdir(self.commands_dir):
            full_path = join(self.commands_dir, g)
            if isdir(full_path):
                self._load_properties_from_commands(full_path, g)
                self.command_groups[g] = full_path
                commands = self._load_commands(full_path)
                self.commands_by_group[g] = commands

    def _load_groups_plans(self):
        self._load_properties_from_plans(self.plans_dir)
        for g in os.listdir(self.plans_dir):
            full_path = join(self.plans_dir, g)
            if isdir(full_path):
                self._load_properties_from_plans(full_path, g)
                self.plan_groups[g] = full_path
                plans = self._load_plans(full_path)
                self.plans_by_group[g] = plans

    def _load_vars(self):
        vars_dir = join(self.environments_dir, self.env, C.VARS_DIR)
        for f in os.listdir(vars_dir):
            utils.ensure_filename(f)
            full_path = join(vars_dir, f)
            if not isdir(full_path) and not utils.is_reserved_word(f):
                self._vars_source[f] = full_path

    def _load_properties_from_plans(self, path, group=C.GLOBALS_NAME):
        full_path = join(path, C.PROPERTIES_NAME)
        if isfile(full_path):
            self._set_plan_properties_source(group, full_path)

    def _load_properties_from_commands(self, path, group=C.GLOBALS_NAME):
        full_path = join(path, C.PROPERTIES_NAME)
        if isfile(full_path):
            self._set_command_properties_source(group, full_path)

    def _set_command_properties_source(self, group, value):
        self.properties_source[C.COMMAND_KEY][group] = value

    def _set_plan_properties_source(self, group, value):
        self.properties_source[C.PLAN_KEY][group] = value

    def _load_plans(self, pl_dir):
        plans = []
        for f in os.listdir(pl_dir):
            utils.ensure_filename(f)
            full_path = join(pl_dir, f)
            if not isdir(full_path) and not utils.is_reserved_word(f):
                plans.append(f)
        return plans

    def _load_commands(self, commands_dir):
        commands = []
        for f in os.listdir(commands_dir):
            utils.ensure_filename(f)
            full_path = join(commands_dir, f)
            if not isdir(full_path) and not utils.is_reserved_word(f):
                commands.append(f)
        return commands
