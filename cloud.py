'''
Created on Mar 24, 2013

@author: mmartin
'''

from base64 import encodestring
from pymez.account import Account
from pymez.authorization import Authorization
from pymez.endpoints import CLOUD_ENDPOINT
from pymez.get_creds import get_creds
from pymez.http import Http
from pymez.location import Location

import json


class Cloud(object):
    '''
    Basic cloud object
    '''

    def __init__(self,
                 userid,
                 url,
                 gdl_env=None,
                 passwd=None):
        '''
        Initialize cloud access.
        '''
        self.account = None
        self.url = '%s%s' % (url, CLOUD_ENDPOINT)
        self.userid = userid
        self.passwd = passwd

        auth = Authorization(self.userid,
                             gdl_env=gdl_env,
                             passwd=self.passwd)

        self.auth_string = auth.get_auth()
        self.headers = {'X-Client-Specification': '3',
                        'Authorization': self.auth_string}

        self.http = Http(self.url,
                         headers=self.headers)
        self._get()

    def _basic_auth(self, user, passwd):
        '''
        Basic Authentication String
        '''
        return 'Basic %s' % encodestring('%s:%s' % (user, passwd)).strip()

    def _gdl_auth(self, userid, env):
        '''
        GDL Authentication String
        '''
        token, _status, _response = get_creds(userid, env)
        return 'GDL gdl_token=%s,gdl_id=' % (token, userid)

    def _get(self):
        '''
        Get the cloud information.
        '''
        status, content, _headers = self.http.GET()
        if not status in [200]:
            return None
        self.cloud_info = json.loads(content)
        self._account_uri = \
            self.cloud_info['cloud']['account']['uri']
        self._allspaces_uri = \
            self.cloud_info['cloud']['allspaces']['uri']
        self._locations = []
        num_locs = len(self.cloud_info['cloud']['locations'])
        for loc in range(num_locs):
            default = \
                self.cloud_info['cloud']['locations'][loc]['default']
            mgmt_uri = \
                self.cloud_info['cloud']['locations'][loc]['mgmt_uri']
            name = \
                self.cloud_info['cloud']['locations'][loc]['name']
            namespace = \
                self.cloud_info['cloud']['locations'][loc]['namespace']
            notifications = \
                self.cloud_info['cloud']['locations'][loc]['notifications']
            root_container = \
                self.cloud_info['cloud']['locations'][loc]['rootContainer']
            spaces = \
                self.cloud_info['cloud']['locations'][loc]['spaces']
            cloud = self
            location = Location(cloud,
                                mgmt_uri,
                                name,
                                namespace,
                                notifications,
                                root_container,
                                spaces,
                                self.headers,
                                default=default)
            self._locations.append(location)
        self._namespaces_uri = self.cloud_info['cloud']['namespaces']['uri']
        self._recyclebin_uri = self.cloud_info['cloud']['recyclebin']['uri']
        self._search_uri = self.cloud_info['cloud']['search']['uri']
        self._shares_uri = self.cloud_info['cloud']['shares']['uri']

    def get_account(self):
        if not self.account:
            self.account = Account(self.pool, self.headers)
        return self.account

    def get_account_uri(self):
        return self._account_uri

    def get_allspaces_uri(self):
        return self._allspaces_uri

    def get_cloud(self):
        return self.cloud_info

    def get_default_location(self):
        for loc in self._locations:
            if loc.isDefault():
                return loc
        return None

    def get_headers(self):
        return self.headers
    
    def get_location(self, idx):
        return self._locations[idx]

    def get_locations(self):
        return self._locations

    def get_location_by_name(self, name):
        for loc in self._locations:
            if name == loc.get_name():
                return loc
        return None

    def get_namespaces_uri(self):
        return self._namespaces_uri

    def get_recyclebin_uri(self):
        return self._recyclebin_uri

    def get_search_uri(self):
        return self._search_uri

    def get_shares_uri(self):
        return self._shares_uri

    def get_location_root_container(self, which=0):
        return self._locations[which].get_root_container()

    def get_location_root_container_uri(self, which=0):
        return self._locations[which].get_root_container_uri

    def get_location_spaces_uri(self, which=0):
        return self._locations[which]['spaces']

    def how_many_locations(self):
        return len(self._locations)
