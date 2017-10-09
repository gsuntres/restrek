import cmd
import sys
import httplib
import restrek.constants as C
from restrek.errors import RestrekError
from restrek.core.context import RestrekContext
from restrek.core.services import PlanService


class RestrekConsole(cmd.Cmd):

    def __init__(self,
                 workspace=C.WS_DIR,
                 env=C.DEFAULT_ENV,
                 verbose=None):
        self.ctx = RestrekContext(workspace, env, verbose)
        cmd.Cmd.__init__(self)

    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            self.do_exit(self)

    def do_exit(self, args):
        """Exit from the console"""
        sys.stdout.write('\n')
        return -1

    def do_run(self, args):
        """Run a plan"""
        if args:
            scheduler = PlanService(self.ctx)
            try:
                plans = args.split(' ')
                scheduler.execute_multiple_plans(plans)
            except RestrekError as e:
                print e
        else:
            print 'specify which plan(s) to run'

    def inspect_attr(self, args):
        STEP_RESERVED_WORDS = ['name', 'except', 'register']
        count = len(args)
        for attr in args:
            if attr in STEP_RESERVED_WORDS:
                print attr

    def do_list(self, args):
        """List plans, groups"""
        if args:
            args_arr = args.split()
            arg1 = args_arr[0]
            if arg1 == 'plans':
                if len(args_arr) > 1:
                    print self.ctx.get_plans(args_arr[1])
                else:
                    print self.ctx.get_plans()
            elif arg1 == 'groups':
                print self.ctx.get_plan_groups()
            else:
                print 'Can not list unknown `%s`' % arg1
        else:
            print '''usage: \n
            list groups
            list plans
            list plans < group >'''

    def do_reload(self, args):
        self.ctx.reload()
        print 'reloading done!'

    do_EOF = do_exit
