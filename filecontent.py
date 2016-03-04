'''
Created on Jul 19, 2013

@author: mmartin
'''

from pymez.http import Http

import sys


class FileContent(object):
    '''
    File content object. Support GET and POST of file content.
    '''

    def __init__(self,
                 fileobj):
        '''
        Constructor
        '''
        self.fileobj = fileobj  # The file object that governs this content.
        self._cloud = self.fileobj._cloud
        self.userid = self._cloud.userid
        self.passwd = self._cloud.passwd
        self._parent = self.fileobj._parent
        self.headers = self._cloud.get_headers()
        self.http = Http(None,
                         headers=self.headers)

    def GET(self):
        '''
        Get the file's content.
        '''
        status, content, headers = self.http.GET()
        return status, content, headers

    def POST(self, fpath):
        '''
        Post the file's content.
        '''
        self.http.files = {self.fileobj.get_name(): open(fpath, 'r')}
        self.http.url = self._parent.get_contents_uri()
        status, _content, headers = self.http.POST()
        if status not in [200, 201]:
            print 'POST failed with %d' % status
            print 'Headers: %s' % headers
            sys.exit(1)
        return True
