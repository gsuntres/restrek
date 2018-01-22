def test_count(sch_command_pg):
    sess = sch_command_pg.execute_plan('misc.test_count')[1]
    print sess.output['data']
    assert 0 == sess.output['data'][0][0]


def test_add(sch_command_pg):
    sess = sch_command_pg.execute_plan('misc.test_insert')[1]
    assert 1 == sess.output['data'][0][0]
