import argparse


class BaseArgumentParser(object):

    def __init__(self):
        p = argparse.ArgumentParser(prog='restrek')
        p.add_argument('-w', '--workspace-dir', help='Workspace location')
        p.add_argument('-v', '--verbose', help='Be very informative', action='store_true')
        p.add_argument('-e', '--env', help='Which environment to use (Default: devel)', default='devel')
        self._opts = p.parse_args()

    @property
    def workspace_dir(self):
        return self._opts.workspace_dir

    @property
    def env(self):
        return self._opts.env

    @property
    def verbose(self):
        return self._opts.verbose

    @property
    def all(self):
        kargs = dict()
        if self.workspace_dir is not None:
            kargs.update(dict(workspace=self.workspace_dir))
        if self.env is not None:
            kargs.update(dict(env=self.env))
        if self.verbose is not None:
            kargs.update(dict(verbose=self.verbose))
        return kargs
