'''
Created on Mar 24, 2013

@author: mmartin
'''
from pymez.accept_header import (
    CONTAINER_INFO,
)
from pymez.container import Container


class Location(object):
    '''
    classdocs
    '''

    def __init__(self,
                 cloud,
                 mgmt_uri,
                 name,
                 namespace,
                 notifications,
                 root_container,
                 spaces,
                 headers={},
                 default=False):
        '''
        Constructor
        '''
        self._cloud = cloud
        self._default = default
        self._mgmt_uri = mgmt_uri
        self._name = name
        self._namespace = namespace
        self._notifications = notifications
        self._root_container_uri = root_container
        self._spaces = spaces
        self._headers = headers
        self._headers['Accept'] = CONTAINER_INFO
        self._root_container = Container(self._cloud,
                                         url=self._root_container_uri,
                                         headers=self._headers
                               )

    def isDefault(self):
        return self._default

    def get_mgmt_uri(self):
        return self._mgmt_uri

    def get_name(self):
        return self._name

    def get_namespace(self):
        return self._namespace

    def get_notifications(self):
        return self._notifications

    def get_root_container(self):
        return self._root_container

    def get_root_container_uri(self):
        return self._root_container_uri

    def get_spaces(self):
        return self._spaces
