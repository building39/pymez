'''
Created on May 12, 2013

@author: mmartin
'''
import traceback


class RestException(Exception):

    def __init__(self, status, *args, **kw):
        self.status = status
        self.contentType = kw.get('ContentType', 'text/plain')
        Exception.__init__(self, *args)
        self._stack = '%s: %s\n%s' % (type(self).__name__, status,
                                      ''.join(traceback.format_stack()[:-1]))

    def __call__(self, env, start_response):
        hdrs = [('Content-Type', self.contentType)]
        if self.status[:3] == '401':
            hdrs.append(('WWW-Authenticate', 'Basic realm="default"'))
        start_response(self.status, hdrs)
        yield self.args[0] if self.args else ''


class BadRequest(RestException):
    """Generic exception when something unknown is wrong with the request"""

    def __init__(self, *args, **kw):
        RestException.__init__(self, '400 Bad Request', *args, **kw)

    def __call__(self, env, start_response):
        return RestException.__call__(self, env, start_response)
