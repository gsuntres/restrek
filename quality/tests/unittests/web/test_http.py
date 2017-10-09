import pytest
from requests import Request


def test_req_ensure_headers_are_set_before_data(req):
    assert '{"foo": "bar"}' == req.data


def test_req_default_http_method(req):
    assert 'GET' == req.http_method


def test_req_http_method(req_post):
    assert 'POST' == req_post.http_method


def test_req_url(req):
    assert 'http://www.thisisatest.test' == req.url


def test_req_headers(req):
    assert {
        'Accept': 'application/json',
        'Cache-Control': 'no-cache'
    } == req.headers


def test_req_return_requests_object(req):
    r = req.requests_object
    assert isinstance(r, Request)
    headers = {
        'Accept': 'application/json',
        'Cache-Control': 'no-cache'
    }
    assert headers == r.headers
    assert '{"foo": "bar"}' == r.data
    assert 'http://www.thisisatest.test' == r.url
    assert {} == r.params


def test_res_body(res):
    assert dict(prop1=1, prop3='hello') == res.body


def test_res_status(res):
    assert 200 == res.status


def test_res_headers(res):
    headers = {
        'Contet-Type': 'application/json',
        'Cache-Control': 'no-cache'
    }
    assert headers == res.headers


def test_res_cookies(res):
    {'mycookie': 'this is my cookie val'} == res.cookies