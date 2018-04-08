import os
import re
import uuid
import ast
import collections
import json
import types
import copy
from datetime import datetime
import restrek.constants as C
from restrek.errors import RestrekError


def is_reserved_word(word):
    return word in C.RESERVED_WORDS


def props(cls):
    return [i for i in cls.__dict__.keys() if i[:1] != '_']


def ensure_filename(filename):
    if is_valid_filename(filename) is None:
        raise RestrekError('%s invalid filename' % filename)


def is_valid_filename(filename):
    return re.search(C.FILENAME_REGEX, filename)


def is_valid_identifier(name):
    """Determines, if string is valid Python identifier."""
    if not isinstance(name, str):
        raise TypeError("expected str, but got {!r}".format(type(name)))

    try:
        root = ast.parse(name)
    except SyntaxError:
        return False

    if not isinstance(root, ast.Module):
        return False

    if len(root.body) != 1:
        return False

    if not isinstance(root.body[0], ast.Expr):
        return False

    if not isinstance(root.body[0].value, ast.Name):
        return False

    if root.body[0].value.id != name:
        return False

    return True


def strip_ext(name):
    f, _ = os.path.splitext(name)
    return f


def split_name(name):
    r"""Commands and plans are identified by their group and their actual name
    So for example if a plan `myplan` is grouped in `mygroup` then its full qualified
    name is `mygroup.myplan`

    this method will extract both group and template name.
    """
    if not name:
        raise RestrekError('can\'t split empty names')

    words = re.split('\.', name)
    if len(words) == 1:
        return None, words[0]
    elif len(words) == 0 or len(words) > 2:
        raise RestrekError('%s not a valid name' % name)
    else:
        return words


def get_group(name):
    g, n = split_name(name)
    return g


def combine_name(group, name):
    return '{}.{}'.format(group, name)


def get_val(data, key, default=None):
    if isinstance(data, dict):
        return data[key] if key in data else default
    else:
        return default


def guid():
    return uuid.uuid4()


def milli2sec(ms):
    return ms / 1000


def utcnow():
    return datetime.utcnow()


def now():
    return datetime.now()


def now_str():
    return now().strftime('%H:%M:%S.%f')[:-3]


def str2dict(data):
    if data:
        if isinstance(data, dict):
            return data
        elif isinstance(data, (str, unicode)):
            try:
                return ast.literal_eval(data.strip())
            except (SyntaxError, ValueError), e:
                print e
                return data
    return data


def trim_all(s):
    return re.sub('[\s+]', '', s)


def deep_update(src, toadd):
    for key, val in toadd.iteritems():
        if isinstance(val, collections.Mapping):
            tmp = deep_update(src.get(key, {}), val)
            src[key] = tmp
        elif isinstance(val, list):
            src[key] = (src.get(key, []) + val)
        else:
            src[key] = toadd[key]
    return src


def merge(a, b, path=None):
    "merges b into a"
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

#
# JSON related
#


def json_load(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )


def json_loads(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def json_dumps(json_data):
    if C.PRETTY_JSON:
        return json.dumps(json_data, indent=2, ensure_ascii=False).encode('utf8')
    else:
        return json.dumps(json_data, ensure_ascii=False).encode('utf8')


def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

# Array utils


def arr_eq(a, b):
    ok = isinstance(a, list) and isinstance(b, list)
    ok = ok and len(a) != 0 and len(b) != 0
    ok = ok and len(set(a).difference(set(b))) == 0
    return ok

# Misc


def isinstance_types(val, tps=[]):
    SupportedTypes = ()
    for t in tps:
        if 'str' == t:
            SupportedTypes += (types.StringType,)
        if 'unicode' == t:
            SupportedTypes += (types.UnicodeType,)
        if 'bool' == t:
            SupportedTypes += (types.BooleanType,)
        if 'int' == t:
            SupportedTypes += (types.IntType,)
        if 'float' == t:
            SupportedTypes += (types.FloatType,)
        if 'long' == t:
            SupportedTypes += (types.LongType,)
        if 'dict' == t:
            SupportedTypes += (types.DictionaryType,)
        if 'None' == t:
            SupportedTypes += (types.NoneType,)

    return isinstance(val, SupportedTypes)


def clone(obj):
    return copy.copy(obj)
