def test_check_plan_groups(ctx):
    plan_groups = ctx.get_plan_groups()
    assert 5 == len(plan_groups)


def test_get_plans(ctx):
    plans = ctx.get_plans()
    assert 6 == len(plans)


def test_get_plans_by_group(ctx):
    plans = ctx.get_plans('group1')
    assert 3 == len(plans)


def test_check_commands_groups(ctx):
    cmd_groups = ctx.get_command_groups()
    assert 5 == len(cmd_groups)


def test_get_commands(ctx):
    cmds = ctx.get_commands()
    assert 7 == len(cmds)


def test_get_commands_by_group(ctx):
    cmds = ctx.get_commands('group2')
    assert 2 == len(cmds)


def test_get_group_properties(ctx):
    d = ctx._get_properties('group2', None, None)
    assert 'www.plan-group2.com' == d['host']
    assert 2546 == d['timeout']


def test_get_group_default_properties(ctx_no_global_properties):
    d = ctx_no_global_properties._get_properties('group1', None, None)
    assert 'localhost' == d['host']
    assert 1000 == d['timeout']


def test_get_group_default_properties(ctx_with_global_properties):
    d = ctx_with_global_properties._get_properties('group1', None, None)
    assert 'www.aplansscopehost.com' == d['host']
    assert 1789 == d['timeout']


def test_compact_properties_simple(ctx):
    p = ctx.compact_properties(dict(foo='bar'))
    assert {'foo': 'bar'} == p


def test_compact_properties_with_plugin(ctx):
    PROPS_WITH_PLUGIN = {
        'prop1': 'global-prop1',
        'prop2': 'global-prop2',
        'http': {
            'prop2': 'http-prop2',
            'prop3': 'http-prop3'
        }
    }

    p = ctx.compact_properties(PROPS_WITH_PLUGIN, 'http')

    EXPECTED_PROPS = {
        'prop1': 'global-prop1',
        'prop2': 'http-prop2',
        'prop3': 'http-prop3'
    }

    assert EXPECTED_PROPS == p


def test_compact_properties_with_env_and_plugin(ctx):
    PROPS_WITH_PLUGIN = {
        'prop1': 'global-prop1',
        'prop2': 'global-prop2',
        'devel': {
            'http': {
                'prop2': 'http-prop2',
                'prop3': 'http-prop3'
            }
        }
    }

    p = ctx.compact_properties(PROPS_WITH_PLUGIN, 'http')

    EXPECTED_PROPS = {
        'prop1': 'global-prop1',
        'prop2': 'http-prop2',
        'prop3': 'http-prop3'
    }

    assert EXPECTED_PROPS == p


def test_compact_properties_with_env(ctx):
    PROPS_WITH_PLUGIN = {
        'prop1': 'global-prop1',
        'prop2': 'global-prop2',
        'devel': {
            'prop2': 'http-prop2',
            'prop3': 'http-prop3'
        }
    }

    p = ctx.compact_properties(PROPS_WITH_PLUGIN)

    EXPECTED_PROPS = {
        'prop1': 'global-prop1',
        'prop2': 'http-prop2',
        'prop3': 'http-prop3'
    }

    assert EXPECTED_PROPS == p


def test_merge_properties(ctx, command_descr):
    cmd = ctx.merge_properties(command_descr, 'group1')
    p = cmd.props
    assert 'a simple lonely prop' == p['prop2']
    assert 'www.plan-group1-plugin.com' == p['host']
    assert not p['secure']
    assert 2311 == p['timeout']
    assert 200 == p['prop1']


def test_merge_properties_command_should_override_plan(ctx, command_descr):
    cmd = ctx.merge_properties(command_descr, plan_group='pgroup1', command_group='cgroup1')
    p = cmd.props
    assert not p['debug']
    assert 20 == p['delay']


def test_merge_properties_command_should_override_plan_with_plugin(ctx, command_descr):
    cmd = ctx.merge_properties(command_descr, plan_group='pgroup1', command_group='cgroup1')
    p = cmd.props
    assert not p['debug']
    assert 20 == p['delay']
    assert 'www.command-cgroup1-env-plugin.com' == p['host']


def test_merge_properties_command_should_override_global(ctx_with_global_properties, command_descr):
    cmd = ctx_with_global_properties.merge_properties(command_descr, plan_group='pgroup1', command_group='cgroup1')
    p = cmd.props
    assert 'host.commanscoped.com' == p['host']
    assert 1789 == p['timeout']


def test_merge_properties_command_should_override_global_with_env(ctx_with_global_properties, command_descr):
    cmd = ctx_with_global_properties.merge_properties(command_descr, plan_group='pgroup1', command_group='cgroup2')
    p = cmd.props
    assert 2999 == p['timeout']
    assert 'host.globalscoped.com' == p['host']
