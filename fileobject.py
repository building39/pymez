'''
Created on Mar 24, 2013

@author: mmartin
'''

import json

from pymez.accept_header import (
    FILE_INFO,
    METADATA,
    METADATA_LIST
)
from pymez.http import Http
from urlparse import urlparse

CHUNK = 64 * 1024


class FileObject(object):
    '''
    classdocs
    '''

    def __init__(self,
                 cloud,
                 headers={},
                 name=None,
                 parent=None,
                 url=None
                 ):
        '''
        Constructor
        '''
        self._cloud = cloud
        self.userid = self._cloud.userid
        self.passwd = self._cloud.passwd
        self.url = url
        self.headers = headers
        self.headers['Accept'] = FILE_INFO

        self._accessed = None  # when last accessed
        self._bytes = 0  # size in bytes
        self._comments = None  # URI of comments
        self._contents = None  # URI of contents
        self._created = None  # when created
        self._metadata = None  # URI of metadata
        self._mime_type = None  # mime type
        self._modified = None  # when last modified
        self._modified_by = None  # who modified it
        self._name = name  # file name
        self._owner = None  # who owns this file
        self._parent = parent  # URI of this file's parent container
        self._permissions = None  # URI of permissions
        self._public = False  # is file public?
        self._shared = False  # is this container shared?
        self._shorturls = None  # URI of short urls
        self._starred = False  # is file starred?
        self._thumbnail = None  # URI of thumbnail
        self._uri = None  # this container's URI
        self._version = None  # what it says
        self._versions = None  # URI of versions
        self.http = Http(self.url,
                         headers=self.headers)
        if self.url:
            self._get()

    def _get(self):
        '''
        Get the file information.
        '''
        headers = self._cloud.get_headers()
        headers['Accept'] = FILE_INFO
        self.http.headers = headers
        self.http.url = self.url
        status, content, headers = self.http.GET()
        if not status in [200]:
            print 'Status1: %d' % status
            print 'URL: %s' % self.url
            print 'headers: %s' % headers
            return None
        self._file_info = json.loads(content)
        self._accessed = \
            self._file_info['file']['accessed']
        self._bytes = \
            self._file_info['file']['bytes']
        self._comments = \
            self._file_info['file']['comments']
        self._content_uri = \
            self._file_info['file']['content']['uri']
        self._created = \
            self._file_info['file']['created']
        self._metadata = \
            self._file_info['file']['metadata']
        self._mimetype = \
            self._file_info['file']['mime_type']
        self._modified = \
            self._file_info['file']['modified']
        self._modified_by = \
            self._file_info['file']['modified_by']
        self._name = \
            self._file_info['file']['name']
        self._owner = \
            self._file_info['file']['owner']
        self._parent = \
            self._file_info['file']['parent']
        self._permissions = \
            self._file_info['file']['permissions']['uri']
        self._public = \
            self._file_info['file']['public']
        self._shared = \
            self._file_info['file']['shared']
        if 'shorturls' in self._file_info['file']:
            self._shorturls = \
                self._file_info['file']['shorturls']['uri']
        if 'starred' in self._file_info['file']:
            self._starred = \
                self._file_info['file']['starred']
        self._thumbnail = \
            self._file_info['file']['thumbnail']
        self._uri = \
            self._file_info['file']['uri']
        self._version = \
            self._file_info['file']['version']
        self._versions = \
            self._file_info['file']['versions']

    def DELETE(self):
        '''
        Delete this file object
        '''
        status, _headers = self.http.DELETE(self._uri)
        return status

    def GET(self):
        '''
        Return the file information as a dictionary.
        '''
        return self._file_info

    def GET_metadata(self, item=None):
        self.http.headers = {'X-Client-Specification': '3',
                   'Authorization': self._cloud.auth_string,
                   'Accept': METADATA_LIST}
        self.http.url = '%s/%s' % (self.get_metadata_uri(), item) if item else self.get_metadata_uri()

        status, content, headers = self.http.GET()
        if status in [200]:
            return (status, json.loads(content), headers)
        else:
            return (status, content, headers)

    def get_accessed(self):
        return self._accessed

    def get_bytes(self):
        return self._bytes

    def get_comments(self):
        return self._comments

    def get_content(self):
        self.http.url = str('%s' % (self._content_uri))
        status, content, headers = self.http.GETSTREAM()

        if not status in [200]:
            print 'Status1: %d' % status
            print 'URL: %s' % self._content_uri
            print 'headers: %s' % headers
            return None

        return status, content

    def get_content_uri(self):
        return self._content_uri

    def get_content_oid(self):
        oid = urlparse(self._content['uri']).path.split('/')[3]
        return oid

    def get_created(self):
        return self._created

    def get_metadata_uri(self):
        return self._metadata['uri']

    def get_mimetype(self):
        return self._mimetype

    def get_modified(self):
        return self._modified

    def get_modified_by(self):
        return self._modified_by

    def get_name(self):
        return self._name

    def get_owner(self):
        return self._owner

    def get_parent(self):
        return self._parent

    def get_permissions(self):
        return self._permissions

    def get_public(self):
        return self._public

    def get_shared(self):
        return self._shared

    def get_shorturls(self):
        return self._shorturls

    def get_starred(self):
        return self._starred

    def get_thumbnail(self):
        return self._thumbnail

    def get_uri(self):
        return self._uri

    def get_version(self):
        return self._version

    def get_versions(self):
        return self._versions

    def PUT(self,
            data,
            content_type='application/vnd.csp.file-info+json',
            uri=None):
        '''
        Update the file-info.
        '''
        # import pydevd; pydevd.settrace()
        self.http.headers = {'X-Client-Specification': '3',
                             'Content-Type': content_type,
                             'Authorization': self._cloud.auth_string}
        self.http.url = uri if uri else self.get_uri()
        if type(data) == dict:
            data = json.dumps(data)
        status, _content, _headers = self.http.PUT(str(data))
        if status in [201, 204]:
            return True
        print 'PUT failed with %d' % status
        print '    uri: %' % self.http.url
        print '    payload: %s' % data
        return False

    def set_metadata(self, name, metadata):
        return self.PUT(metadata,
                        content_type=METADATA,
                        uri='%s/%s' % (self.get_metadata_uri(), name))


class FileObjectStream:

    def __init__(self, response):
        self.response = response

    def read(self):
        chunk = self.response.read(CHUNK)
        return chunk

    def close(self):
        pass
