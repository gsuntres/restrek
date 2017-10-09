def test_properties_command_should_override_plan(sch):
    sess = sch.execute_plan('pgroup1.plan1')[0]
    assert sess.output['command_properties']['show_props']
    assert not sess.output['command_properties']['debug']
