'''
Created on Jul 19, 2013

@author: mmartin
'''

# import human_curl as requests

import requests
import sys
from urllib2 import Request, urlopen

from poster.encode import multipart_encode  # $ pip install poster
from poster.streaminghttp import register_openers

register_openers()  # install openers globally


def report_progress(param, current, total):
    sys.stdout.write("\r%03d%% of %d" % (int(1e2 * current / total + .5), total))


class Http(object):
    '''
    For all things http.
    '''

    def __init__(self,
                 url,
                 data=None,
                 files=None,
                 headers=None):
        '''
        Constructor
        '''
        self.data = data
        self.files = files
        if not headers:
            self.headers = {}
        else:
            self.headers = headers
        self.url = url
        if not type(self.url) == str:
            self.url = str(self.url)
        if self.url and not self.url.endswith('/'):
            self.url = '%s/' % self.url
            
        #import httplib
        #httplib.HTTPConnection._http_vsn = 10
        #httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

    def GET(self):
        r = requests.get(self.url,
                         allow_redirects=True,
                         headers=self.headers)
        return r.status_code, r.content, r.headers

    def GETSTREAM(self):
        r = requests.get(self.url,
                         allow_redirects=True,
                         headers=self.headers,
                         stream=True)
        return r.status_code, r.raw, r.headers

    def DELETE(self, url=None):
        r = requests.delete(url if url else self.url,
                            allow_redirects=True,
                            headers=self.headers)
        return r.status_code, r.headers

    def HEAD(self):
        r = requests.head(self.url,
                          allow_redirects=True,
                          headers=self.headers)
        return r.status_code, r.headers

    def POST(self):
        if self.files:
            request = Request(self.url, *multipart_encode(self.files, cb=report_progress))
        elif self.data:
            request = Request(self.url, self.data)
        else:
            return 406
        for h in self.headers:
            request.add_header(h, self.headers[h])
        r = urlopen(request)

        return r.code, r.read(), r.headers

    def PUT(self, data):
        r = requests.put(self.url,
                         allow_redirects=True,
                         data=data,
                         headers=self.headers)
        return r.status_code, r.raw, r.headers

