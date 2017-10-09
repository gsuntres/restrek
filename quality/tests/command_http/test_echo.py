def test_echo(sch):
    sess = sch.execute_plan('misc.echo')[0]
    assert 'Hello there' == sess.output['msg']
