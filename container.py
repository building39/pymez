'''self._auth = self._cloud.auth
Created on Mar 24, 2013

@author: mmartin
'''

from pymez.accept_header import (
    CONTAINER_INFO,
    FILE_LIST,
    METADATA,
    METADATA_LIST
)
from pymez.fileobject import FileObject
from pymez.http import Http

import json
import sys
from urlparse import urlparse

COUNT = 1000


class Container(object):
    '''
    Representation of container information.    '''

    def __init__(self,
                 cloud,
                 parent=None,
                 url=None,
                 headers={},
                 name=None):
        '''
        Constructor
        '''
        self._cloud = cloud
        self.user = self._cloud.userid
        self.passwd = self._cloud.passwd
        self.url = str(url)
        self.headers = headers

        self._containers = []  # a list of sub-containers in this container
        self._objects = []  # a list of objects in this container

        self._accessed = None  # when last accessed
        self._bytes = 0  # size in bytes
        self._comments = None  # URI of comments
        self._contents = None  # URI of contents
        self._created = None  # when created
        self._metadata = None  # URI of metadata
        self._modified = None  # when last modified
        self._modified_by = None  # who modified it
        self._name = name  # container name
        self._owner = None  # who owns this container
        #self._owner_principal = None  # who owns this container
        self._parent = parent  # URI of this container's parent
        self._permissions = None  # URI of permissions
        self._principal = None  # permissions principal
        self._simple = None  # simple permissions
        self._shared = False  # is this container shared?
        self._uri = None  # this container's URI
        self._version = None  # what it says
        self.http = Http(self.url,
                         headers=self.headers)

        if self._parent:
            self._create()
        self._get()

    def DELETE(self):
        '''
        Delete this container object
        '''
        status, _headers = self.http.DELETE(self._uri)
        return status

    def GET(self):
        '''
        Return the container information as a dictionary.
        '''
        return self._container_info

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

    def _create(self):
        self.http.data = '{"container": {"name": "%s"}}' % self._name
        self.http.headers = {'X-Client-Specification': '3',
                   'Authorization': self._cloud.auth_string,
                   'Accept': CONTAINER_INFO,
                   'Content-Type': CONTAINER_INFO}
        self.http.url = str('%s/contents' % self._parent)
        status, content, headers = self.http.POST()
        if status in [201]:
            self.url = content.strip()  # lose the trailing whitespace
            self._uri = self.url
        else:
            print 'Status1: %d' % status
            print 'URL: %s' % self.http.url
            print 'headers: %s' % headers
            sys.exit()

    def _get(self):
        '''
        Get the container information.
        '''
        headers = self._cloud.get_headers()
        headers['Accept'] = CONTAINER_INFO
        self.http.headers = headers
        self.http.url = self.url
        status, content, headers = self.http.GET()
        if not status in [200]:
            print 'Status1: %d' % status
            print 'URL: %s' % self.url
            print 'headers: %s' % self.headers
            return None
        self._container_info = json.loads(content)
        self._accessed = \
            self._container_info['container']['accessed']
        self._bytes = \
            self._container_info['container']['bytes']
        self._comments = \
            self._container_info['container']['comments']
        self._contents = \
            self._container_info['container']['contents']
        self._created = \
            self._container_info['container']['created']
        self._metadata = \
            self._container_info['container']['metadata']
        self._modified = \
            self._container_info['container']['modified']
        self._modified_by = \
            self._container_info['container']['modified_by']
        self._name = \
            self._container_info['container']['name']
        self._owner = \
            self._container_info['container']['owner']
        #self._owner_principal = \
        #    self._container_info['container']['owner_principal']
        self._parent = \
            self._container_info['container']['parent']
        self._permissions = \
            self._container_info['container']['permissions']['uri']
        self._principal = \
            self._container_info['container']['permissions']['principal']
        self._simple = \
            self._container_info['container']['permissions']['simple']
        self._shared = \
            self._container_info['container']['shared']
        self._uri = \
            self._container_info['container']['uri']
        self._version = \
            self._container_info['container']['version']

    def _get_contents(self, depth=1):
        self._containers = []
        self._objects = []
        headers = {'X-Client-Specification': '3',
                   'Authorization': self._cloud.auth_string}
        headers['Accept'] = FILE_LIST
        headers['X-Cloud-Depth'] = '1'
        self.http.headers = headers
        self.http.url = '%s/%s' % (self.url, 'contents?search')
        status, content, headers = self.http.GET()
        if not status in [200]:
            print 'Status2: %d' % status
            print 'URL: %s' % self.url
            print 'headers: %s' % self.headers
            return None
        contents = json.loads(content)
        # return contents
        total = contents['file-list']['total']

        processed = 0
        while processed < total:
            num_this_time = 0

            count = contents['file-list']['count']
            for x in range(count):
                num_this_time = len(contents['file-list']['file-list'])
                if 'container' in contents['file-list']['file-list'][x]:
                    sub = Container(
                        self._cloud,
                        url=contents['file-list']['file-list'][x]['container']['uri'],
                        headers=self.headers)
                    self._containers.append(sub)
                elif 'file' in contents['file-list']['file-list'][x]:
                    obj = FileObject(
                        self._cloud,
                        url=contents['file-list']['file-list'][x]['file']['uri'],
                        headers=self.headers)
                    self._objects.append(obj)
                else:
                    continue
            processed += num_this_time
            if processed < total:
                newurl = '%s&start=%d&count=%d' % (self.url, processed, COUNT)
                response = self._pool.urlopen('GET',
                                         newurl,
                                         headers=headers)
                if not response.status in [200]:
                    print 'Status3: %d' % response.status
                    print 'URL: %s' % self.url
                    print 'headers: %s' % headers
                contents = json.loads(response.data)
        return self._containers, self._objects, total

    def get_accessed(self):
        return self._accessed

    def get_bytes(self):
        return self._bytes

    def get_cloud(self):
        return self._cloud

    def get_comments(self):
        return self._comments

    def get_contents(self):
        return self._get_contents()

    def get_contents_oid(self):
        oid = urlparse(self._contents['uri']).path.split('/')[3]
        return oid

    def get_contents_uri(self):
        return self._contents['uri']

    def get_created(self):
        return self._created

    def get_metadata_uri(self):
        return self._metadata['uri']

    def get_modified(self):
        return self._modified

    def get_modified_by(self):
        return self._modified_by

    def get_name(self):
        return self._name

    def get_notifications(self):
        return self._notifications

    def get_objects(self):
        return self._objects

    def get_owner(self):
        return self._owner

    def get_parent(self):
        return self._parent

    def get_permissions(self):
        return self._permissions

    def get_principal(self):
        return self._principal

    def get_shared(self):
        return self._shared

    def get_simple(self):
        return self._simple

    def get_subcontainers(self):
        return self._containers

    def get_uri(self):
        return self._uri

    def get_version(self):
        return self._version

    def PUT(self,
            data,
            content_type='application/vnd.csp.container-info+json',
            uri=None):
        '''
        Update container-info.
        '''
        self.http.headers = {'X-Client-Specification': '3',
                             'Content-Type': content_type,
                             'Authorization': self._cloud.auth_string}
        self.http.url = uri if uri else self.get_uri()
        if type(data) == dict:
            data = json.dumps(data)
        status, _content, _headers = self.http.PUT(data)
        if status in [201, 204]:
            return True
        else:
            print 'Container PUT failed with %d' % status
            print '    uri: %s' % self.http.url
            print '    payload: %s' % data
            return False

    def set_metadata(self, name, metadata):
        return self.PUT(metadata,
                        content_type=METADATA,
                        uri='%s/%s' % (self.get_metadata_uri(), name))

