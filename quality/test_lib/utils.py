import sys
import os
from os.path import isdir, join, abspath, dirname, exists
from restrek.utils.file_utils import copytree


def copy_main_workspace(path, sample='normal'):
    main_ws_path = join(dirname(__file__), '..', 'sample_ws', sample)
    copytree(main_ws_path, path)
