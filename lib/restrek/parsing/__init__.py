import yaml
import re
from os.path import join, exists, getmtime, split
from jinja2 import TemplateNotFound, Environment, BaseLoader
from jinja2.loaders import split_template_path
import restrek.utils as utils
import restrek.parsing.filters


class BaseFileTemplateLoader(BaseLoader):

    def __init__(self, searchpath, encoding='utf-8'):
        self.path = searchpath
        self.encoding = encoding

    def get_source(self, environment, template):
        return self._do_get_source(environment, template)

    def _do_get_source(self, environment, template):
        path = join(self.path, template)
        ok = exists(path)

        if not ok:
            for ext in ['.yaml', '.yml']:
                p = path + ext
                if exists(p):
                    path = p
                    ok = True
                    break

        if not ok:
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with file(path) as f:
            source = f.read().decode('utf-8')
        return source, path, lambda: mtime == getmtime(path)


class FileTemplateLoader(BaseFileTemplateLoader):

    def get_source(self, environment, template):
        g, f = utils.split_name(template)
        if not g:
            raise TemplateNotFound("no groups provided for %s" % template)
        return self._do_get_source(environment, join(g, f))


class PropertiesTemplateLoader(BaseFileTemplateLoader):
    pass


class JinjaEnvironment(Environment):

    def __init__(self, loader=None):
        super(JinjaEnvironment, self).__init__(loader=loader)
        self.filters['combine'] = filters.combine


# YAML


def yaml_load_file(path, encoding='utf-8'):
    with file(path) as f:
        source = f.read().decode(encoding)
    return yaml_load(source)


def yaml_load(source):
    try:
        return yaml.load(source)
    except yaml.YAMLError, exc:
        print 'YAML Error: %s' % exc
        raise


def yaml_dump(data, encoding='utf-8'):
    INT_PATTERN = '\!\!int\s\"(\d+|)\"'

    def int_repl(matchobj):
        return matchobj.group(1)

    try:
        s = yaml.dump(
            data,
            default_style='"',
            width=1000,
            encoding=encoding)
        s = re.sub(INT_PATTERN, int_repl, s)
        # print '[OBJECT] %r -> [STRING] %s' % (data, s)
        return s
    except yaml.YAMLError, exc:
        print exc
        raise
