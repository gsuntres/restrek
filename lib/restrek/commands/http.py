import json
from requests import Session
from requests.exceptions import ConnectionError
from requests.utils import dict_from_cookiejar
from restrek.errors import RestrekError
from restrek.core import RestrekCommand, DEFAULT_KEY
from restrek.utils import milli2sec
from restrek.web.http import HttpResponse, HttpRequest
# supress ssl verify warning
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


SCHEMA_IN = {
    'host': {
        'desc': 'url to call',
        DEFAULT_KEY: 'localhost'
    },
    'secure': {
        'desc': 'should try a secure connection',
        DEFAULT_KEY: False
    },
    'timeout': {
        'desc': 'if supported the command should use it (in ms)',
        DEFAULT_KEY: 1000
    },
    'url': {
        'desc': 'url to call',
        DEFAULT_KEY: '/'
    },
    'method': {
        'desc': 'GET, POST, etc',
        DEFAULT_KEY: 'GET'
    },
    'headers': {
        'desc': 'Headers to use in the requests',
        DEFAULT_KEY: dict()
    },
    'ssl_verify': {
        'desc': 'should verify certificates',
        DEFAULT_KEY: True
    }
}

SCHEMA_OUT = {
    'status': 'the status code returned',
    'body': 'the body returned from the http call',
    'headers': 'response headers',
    'cookies': 'response cookies'
}


class HttpCommand(RestrekCommand):

    def __init__(self, name, props, payload):
        RestrekCommand.__init__(self, name, props, payload, SCHEMA_IN, SCHEMA_OUT)
        self.sess = Session()
        self.sess.verify = self.ssl_verify
        self.resp = None

    def run(self):
        urischema = 'https://' if self.secure else 'http://'
        url = '{}{}{}'.format(urischema, self.host, self.url)
        req = HttpRequest(http_method=self.method, url=url, data=self.payload, headers=self.headers)
        self.log(req)
        try:
            self.set_response(self.do_run(req, self.timeout))
        except ConnectionError as e:
            print e
        except TypeError as e:
            print e

    def do_run(self, request, timeout=1000):
        req = request.requests_object
        p = req.prepare()
        r = self.sess.send(p, timeout=milli2sec(timeout))
        try:
            body = json.loads(r.text)
        except Exception as e:
            print 'JSON %r' % e
            body = r.text

        return {
            'body': body,
            'headers': r.headers,
            'cookies': r.cookies,
            'status': r.status_code
        }

    def set_response(self, data):
        self.resp = HttpResponse.from_data(data)
        self.log(self.resp)
        self.output = data

    def parse_registration_statements(self, registration_statements):
        vars_to_add = dict()
        ctx = dict(body=self.resp.body, status=self.resp.status,
                   cookies=dict_from_cookiejar(self.resp.cookies), headers=self.resp.headers)
        try:
            for key in registration_statements:
                v = self.parse_registration_statement(key, registration_statements[key], ctx)
                vars_to_add.update(v)
        except Exception:
            raise
        return vars_to_add


command = HttpCommand
