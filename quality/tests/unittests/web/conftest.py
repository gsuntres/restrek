import pytest
from restrek.web.http import HttpRequest, HttpResponse


@pytest.fixture(scope='session')
def req():
    headers = {
        'Accept': 'application/json',
        'Cache-Control': 'no-cache'
    }
    data = dict(foo='bar')
    return HttpRequest(url='http://www.thisisatest.test', data=data, headers=headers)


@pytest.fixture(scope='session')
def req_post():
    headers = {
        'Contet-Type': 'application/json'
    }
    data = dict(foo='bar')
    return HttpRequest(http_method='POST', url='http://www.thisisatest.test', data=data, headers=headers)


@pytest.fixture(scope='session')
def res():
    data = {
        'headers': {
            'Contet-Type': 'application/json',
            'Cache-Control': 'no-cache'
        },
        'cookies': {
            'mycookie': 'this is my cookie val'
        },
        'body': '{"prop1": 1,"prop3":"hello"}',
        'status': 200
    }
    return HttpResponse.from_data(data)