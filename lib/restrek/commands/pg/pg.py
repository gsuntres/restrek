import psycopg2
from restrek.errors import RestrekError
from restrek.core import RestrekCommand, DEFAULT_KEY


SCHEMA_IN = {
    'host': {
        'desc': 'host address',
        DEFAULT_KEY: 'localhost'
    },
    'port': {
        'desc': 'connection port number',
        DEFAULT_KEY: 5432
    },
    'user': {
        'desc': 'user name used to authenticate'
    },
    'password': {
        'desc': 'password used to authenticate'
    },
    'dbname': {
        'desc': 'the database name'
    },
    'secure': {
        'desc': 'should try a secure connection',
        DEFAULT_KEY: False
    },
    'timeout': {
        'desc': 'if supported the command should use it (in ms)',
        DEFAULT_KEY: 1000
    },
    'query': {
        'desc': 'the query to execute'
    },
    'expect': {
        'desc': 'describe what kind of types to expect',
        DEFAULT_KEY: []
    }
}

SCHEMA_OUT = {
    'data': 'the data returned'
}


class PgCommand(RestrekCommand):

    def __init__(self, name, props, payload):
        RestrekCommand.__init__(self, name, props, payload, SCHEMA_IN, SCHEMA_OUT)
        self.conn = None
        try:
            self.conn = psycopg2.connect(dbname=self.dbname,
                                    user=self.user,
                                    host=self.host,
                                    port=self.port,
                                    password=self.password)
        except Exception, e:
            print e

    def run(self):
        results = self.do_run(self.query)
        self.log(results)
        self.output = results

    def do_run(self, query):
        cur = self.conn.cursor()
        results = []
        try:
            self.log(self.query)
            cur.execute(self.query)
            for rec in cur.fetchall():
                results.append(rec)
        except psycopg2.ProgrammingError as e:
            print 'Warning: %s' % e
        except:
            raise
        finally:
            print cur.statusmessage
            self.conn.commit()
            self.conn.close()

        return {
            'data': results
        }

