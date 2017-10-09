
def test_add_to_vars(vars_mgr):
    vars_mgr.update(dict(name='George'))
    v = vars_mgr.registered
    assert 'George' == v['name']


def test_unicode_vars(vars_mgr):
    vars_mgr.update({'loggedin_user': {u'username': u'test2@test.com', u'preferredOrg': u'EZp80q7kWLlJ'}})
    v = vars_mgr.registered
    assert {'preferredOrg': 'EZp80q7kWLlJ', 'username': 'test2@test.com'} == v['loggedin_user']


def test_add_none(vars_mgr):
    before_v = vars_mgr.registered
    vars_mgr.update(None)
    v = vars_mgr.registered
    assert before_v == v
