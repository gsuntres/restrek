import sys
import os
from setuptools import setup, find_packages
sys.path.insert(0, os.path.abspath('lib'))
from restrek.release import __version__, __author__, __email__

sys.path.insert(0, os.path.abspath('quality'))
from test_lib import TestRunner


# add pytest_runner only if requested
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
# pytest_runner = ['pytest'] if needs_pytest else []

with open('requirements.txt') as requirements_file:
    install_req = requirements_file.read().splitlines()
    if not install_req:
        print("Problem reading requirements.txt")
        sys.exit(1)

# search commands dir for requirements.txt
cmd_full_path = os.path.abspath(os.path.join('lib', 'restrek', 'commands'))
for cmd_dir_name in os.listdir(cmd_full_path):
    cmd_dir = os.path.join(cmd_full_path, cmd_dir_name)
    if os.path.isdir(cmd_dir):
        req_path = os.path.join(cmd_dir, 'requirements.txt')
        if os.path.exists(req_path):
            with open(req_path) as requirements_file:
                if install_req:
                    print 'Include requirements.txt from %s' % cmd_dir
                    install_req += requirements_file.read().splitlines()


setup(name='restrek',
      version=__version__,
      description='A simple yet powerful RESTful API testing framework',
      author=__author__,
      author_email=__email__,
      license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing'
      ],
      keywords='test testing testing-tools integration-testing rest-api rest api',
      zip_safe=False,
      install_requires=install_req,
      package_dir={'': 'lib'},
      packages=find_packages('lib'),
      # setup_requires=[] + pytest_runner,
      tests_require=['pytest', 'docker', 'mock'],
      cmdclass={'test': TestRunner},
      scripts=[
          'bin/restrek',
          'bin/restrek-console',
          'bin/restrek-init'
      ]
      )
