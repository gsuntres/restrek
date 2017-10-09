def test_cookies(sch):
    sess = sch.execute_plan('cookies.get_cookies')[0]
    assert 'thisisthecookie1' == sess.registered['cookie1']
    assert 'thisisthecookie2' == sess.registered['cookie2']


def test_status(sch):
    sess = sch.execute_plan('misc.check_status200')[0]
    assert 200 == sess.output['status']


def test_body(sch):
    sess = sch.execute_plan('body.get_body')[0]
    assert {'foo': 'bar'} == sess.registered['foobarbody']


def test_headers(sch):
    sess = sch.execute_plan('headers.get_headers')[0]
    assert 'thisiscustomheader1' == sess.registered['header1']
    assert 'thisiscustomheader2' == sess.registered['header2']
    assert 'thisiscustomheader3' == sess.registered['header3']


def test_url_param(sch):
    sess = sch.execute_plan('body.get_entity_by_id')[0]
    assert {'id': '10', 'name': 'Entity Name'} == sess.registered['entity_retrieved_by_id']


def test_http_post(sch):
    sess = sch.execute_plan('body.test_http_post')[0]
    assert {'id': 20, 'name': 'A name', 'age': 80} == sess.registered['posted_data']


def test_append_to_var(sch):
    sess = sch.execute_plan('body.append_to_var')[0]
    assert {'anotherkey': 'anotherval', 'foo': 'bar'} == sess.registered['entity_to_append_to']
