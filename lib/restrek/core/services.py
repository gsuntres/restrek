import sys
from restrek.parsing.dataloader import DataLoader
from restrek.core import Plan, StepSession, CommandDescription, QualifierName
from restrek.tests import TestsManager
import restrek.constants as C
from restrek.utils import split_name, get_group
from restrek.core.display import display


class PlanService:

    def __init__(self, ctx):
        self.ctx = ctx
        self.tests_mgr = TestsManager()
        self.should_continue = True

    def execute_multiple_plans(self, plans):
        sessions = []
        for plan in plans:
            if self.should_continue:
                sessions.append(self.execute_plan(plan))
            else:
                break

        self.ctx.reload()
        return sessions

    def execute_plan(self, name):
        step_sessions = []
        plan_qname = QualifierName.from_string(name)
        display.title_big('Running plan %s' % plan_qname.qualifier)
        plan_obj = self.ctx.load_plan(plan_qname.qualifier)
        plan = Plan(plan_obj, plan_qname)

        for step_obj in plan:
            command = None
            if C.COMMAND_KEY in step_obj:
                command_qname = QualifierName.from_string(step_obj[C.COMMAND_KEY])
                command_obj = self.ctx.load_cmd(command_qname.qualifier)
                command_descr = CommandDescription.from_raw(command_obj)
                command = self.ctx.merge_properties(command_descr, plan_qname.group, command_qname.group)
            step = self.ctx.load_step(step_obj)

            # create step session
            sess = StepSession(step, command)

            if sess.properties is not None and isinstance(sess.properties, dict):
                command.props.update(self.ctx.compact_properties(sess.properties, command_descr.plugin))

            step_sessions.append(sess)
            if not sess.skip:
                display.title('Invoking step %s' % sess.name)
                self._before_commit(sess)
                sess.commit()
                self._after_commit(sess)

                if sess.runnable_command is not None:
                    display.log('step %s finished in %s ms' % (sess.name, sess.duration))

                if not self.should_continue:
                    break

        return step_sessions

    def _run_tests(self, tests, data):
        if tests and isinstance(tests, dict):
            for a in tests.keys():
                test_succeeded = self._run_test(a, tests[a], data)
                if not test_succeeded and not C.CONTINUE_ON_FAIL:
                    self.should_continue = False
                    break

    def _before_commit(self, sess):
        pass

    def _after_commit(self, sess):
        # set about tests
        if sess.tests and len(sess.tests) > 0 and isinstance(sess.tests, list):
            gen = self.tests_mgr.assert_tests(sess.tests, sess.output)
            for test_succeeded in gen:
                if not test_succeeded and not C.CONTINUE_ON_FAIL:
                    self.should_continue = False
                    break

        # update registered variables
        self.ctx.add_to_vars(sess.registered)

    def _load_step(self, name):
        return Step.from_raw(self.ctx.load_step(name))
