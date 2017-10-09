from os.path import join, exists
import jinja2
from jinja2 import TemplateNotFound, Template
import restrek.utils as utils
from restrek.errors import RestrekError
from restrek.parsing import FileTemplateLoader, PropertiesTemplateLoader, JinjaEnvironment, yaml_load_file, yaml_load, yaml_dump
import restrek.constants as C


class DataLoader:

    def __init__(self, commands_dir, plans_dir):
        self.commands_dir = commands_dir
        self.plans_dir = plans_dir
        self.templates = []
        self.default_env = JinjaEnvironment()
        self.cmds_env = None
        self.properties_env = None
        self._init_jinja()

    def _init_jinja(self):
        self.cmds_env = JinjaEnvironment(loader=FileTemplateLoader(self.commands_dir))
        self.properties_env = JinjaEnvironment(loader=PropertiesTemplateLoader(self.plans_dir))

    def load_plan(self, name):
        g, f = utils.split_name(name)
        path = join(self.plans_dir, g, f)
        if not exists(path):
            raise RestrekError('Plan %s does not exist (%s)' % (name, path))
        return yaml_load_file(path)

    def load_step(self, obj, data=None):
        source = yaml_dump(obj)
        tpl = self.default_env.from_string(source)
        output = tpl.render(data) if data else tpl.render()
        return yaml_load(output)

    def load_cmd(self, name, data=None):
        output = self._do_load(self.cmds_env, name, data)
        return output

    def load_properties(self, file, data=None):
        output = self._do_load(self.properties_env, file, data)
        return output

    def _do_load(self, env, name, data=None):
        try:
            tpl = env.get_template(name)
        except TemplateNotFound:
            raise RestrekError('%s not found' % name)
        output = tpl.render(data) if data else tpl.render()

        return yaml_load(output)
