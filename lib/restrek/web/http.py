from requests import Request
from restrek.utils.web_utils import is_json as is_json
from restrek.utils import get_val, str2dict, json_loads, json_dumps


class HttpRequest(object):

    def __init__(self, url, http_method='GET', data=None, headers=dict()):
        self.url = url
        self.http_method = http_method
        self.headers = headers
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if data:
            self._data = self._dump_data(data)
        else:
            self._data = None

    @property
    def requests_object(self):
        if self._data:
            req = Request(self.http_method, self.url, data=self._data, headers=self.headers)
        else:
            req = Request(self.http_method, self.url, headers=self.headers)
        return req

    def _dump_data(self, data):
        _d = ''
        try:
            _d = json_dumps(str2dict(data)) if is_json(self.headers) else data
        except Exception as e:
            print 'can\'t dump %s' % e.message

        return _d

    def __str__(self):
        s = '[REQUEST]'
        s += '\n{} {}'.format(self.http_method, self.url)
        if self._data:
            s += '\npayload:'
            p = ''
            try:
                p = self.data
            except Exception as e:
                print e
            s += '\n {}'.format(p)
        if self.headers and len(self.headers) != 0:
            s += '\nheaders: '
            for h in self.headers.keys():
                s += '\n- {}: {}'.format(h, self.headers[h])
        return s


class HttpResponse(object):

    def __init__(self, body=None, headers=dict(), cookies=dict(), status=None):
        self.headers = headers
        self.body = body
        self.status = status
        self.cookies = cookies

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, val):
        self._body = json_loads(val) if is_json(self.headers) and isinstance(val, (str, unicode)) else val

    @classmethod
    def from_data(cls, data):
        headers = get_val(data, 'headers', dict())
        body = get_val(data, 'body', None)
        cookies = get_val(data, 'cookies', dict())
        status = get_val(data, 'status')

        return cls(body, headers, cookies, status)

    def __str__(self):
        s = '[RESPONSE]'
        s += '\nstatus: {}'.format(self.status)
        s += '\nbody:'
        p = ''
        try:
            p = json_dumps(self.body)
        except Exception as e:
            p = self.body
        s += '\n {}'.format(p)
        s += '\nheaders:'
        for h in self.headers.keys():
            s += '\n- {}: {}'.format(h, self.headers[h])
        if self.cookies and len(self.cookies) != 0:
            s += '\ncookies:'
            for c in self.cookies.keys():
                s += '\n- {} : {}'.format(c, self.cookies[c])
        return s
