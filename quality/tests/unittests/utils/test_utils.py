import pytest
import restrek.utils as utils
from restrek.errors import RestrekError


def test_ensure_filename_with_dot():
    with pytest.raises(RestrekError):
        utils.ensure_filename('skjafldas.dfadfda')


def test_ensure_filename_with_special_char():
    with pytest.raises(RestrekError):
        utils.ensure_filename('skjaf?asdfadfda')


def test_strip_ext():
    f = utils.strip_ext('filewithext.ext')
    assert 'filewithext' == f


def test_strip_ext_already_no_ext():
    f = utils.strip_ext('filewithext')
    assert 'filewithext' == f


def test_split_name():
    g, n = utils.split_name('foo.bar')
    assert 'foo' == g
    assert 'bar' == n


def test_get_group():
    g = utils.get_group('foo.bar')
    assert 'foo' == g


def test_split_name_nogroup():
    g, n = utils.split_name('bar')
    assert g is None
    assert 'bar' == n


def test_split_name_throws_when_none():
    with pytest.raises(RestrekError):
        utils.split_name(None)


def test_split_name_throws_when_invalid_format():
    with pytest.raises(RestrekError):
        utils.split_name('foo.bar.foo')


def test_combine_name():
    assert utils.combine_name('foo', 'bar') == 'foo.bar'


def test_trim_all():
    s = 'val1, val2,     val3'
    assert 'val1,val2,val3' == utils.trim_all(s)


def test_trim_all_with_new_line():
    s = 'val1, \n val2, \n\n    val3'
    assert 'val1,val2,val3' == utils.trim_all(s)


def test_arr_eq_empty_arrays():
    a = []
    b = []
    ok = utils.arr_eq(a, b)
    assert not ok


def test_arr_eq_one_empty():
    a = [1, 2, 3]
    b = []
    ok = utils.arr_eq(a, b)
    assert not ok


def test_arr_eq_not_equal():
    a = [1, 2, 3]
    b = [1, 2, 4]
    ok = utils.arr_eq(a, b)
    assert not ok


def test_arr_eq_equal():
    a = [1, 2, 3]
    b = [1, 2, 3]
    ok = utils.arr_eq(a, b)
    assert ok
