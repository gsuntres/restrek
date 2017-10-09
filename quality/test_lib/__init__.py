import sys
import os
import shlex
import pytest
import errno

from setuptools.command.test import test as TestCommand
from test_lib.docker_mgr import spin_up


class TestRunner(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]
    base_args = '--maxfail=1 -rf '

    def initialize_options(self):
        self.utilize_tests()
        TestCommand.initialize_options(self)

    def run_tests(self):
        for test in self.tests_has_image:
            ok = True
            if self.tests_has_image[test]:
                ok = self.spinup_image(test)
            if ok:
                print 'will run %s' % test
                errn = self.run_pytest(test)
                if errno.ENOENT == errn:
                    break
            else:
                print 'will skip %s' % test

    def run_pytest(self, test):
        return pytest.main(shlex.split('{} quality/tests/{}'.format(TestRunner.base_args, test)))

    def utilize_tests(self):
        self.tests_has_image = dict()
        for test in self.test_dirs:
            self.tests_has_image[test] = test in self.images_dir

    def spinup_image(self, test):
        return spin_up(test)

    @property
    def test_dirs(self):
        test_dirs = []
        root_dir = os.path.join(os.path.dirname(__file__), '..', 'tests')
        for file in os.listdir(root_dir):
            if os.path.isdir(os.path.join(root_dir, file)) and file not in ['__pycache__']:
                test_dirs.append(file)

        return test_dirs

    @property
    def images_dir(self):
        images_dir = []
        root_dir = os.path.join(os.path.dirname(__file__), '..', 'images')
        for file in os.listdir(root_dir):
            if os.path.isdir(os.path.join(root_dir, file)):
               images_dir.append(file)

        return images_dir
