from os import makedirs, stat, listdir
from os.path import exists, join, isdir
from shutil import copy2


def copytree(src, dst, symlinks=False, ignore=None):
    if not exists(dst):
        makedirs(dst)
    for item in listdir(src):
        s = join(src, item)
        d = join(dst, item)
        if isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not exists(d) or stat(s).st_mtime - stat(d).st_mtime > 1:
                copy2(s, d)
