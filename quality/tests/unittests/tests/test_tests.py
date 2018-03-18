
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


def test_uuid_regex_ok(tests_mgr):
    r = tests_mgr.assert_tests(["assert_regex('798397d4-f8a0-11e7-8ca1-14dae90eaa0a', '[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}')"], dict())
    v = r.next()
    assert isinstance(v, bool)
    assert v


def test_uuid_regex_failed(tests_mgr):
    r = tests_mgr.assert_tests(["assert_regex('98397d4-f8a0-11e7-8ca1-14dae90eaa0a', '[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}')"], dict())
    v = r.next()
    assert isinstance(v, bool)
    assert not v


def test_assert_ex_ok(tests_mgr):
    r = tests_mgr.assert_tests(["assert_ex(status)"], dict(status=202))
    v = r.next()
    assert isinstance(v, bool)
    assert v
