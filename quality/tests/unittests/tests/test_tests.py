
def test_equals_ok(tests_mgr):
    r = tests_mgr.assert_tests(["assert_eq(200, status)"], dict(status=200))
    v = r.next()
    assert isinstance(v, bool)
    assert v


def test_equals_failed(tests_mgr):
    r = tests_mgr.assert_tests(["assert_eq(201, status)"], dict(status=200))
    v = r.next()
    assert isinstance(v, bool)
    assert not v
