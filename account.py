'''
Created on Mar 24, 2013

@author: mmartin
'''
from pymez.accept_header import ACCOUNT_INFO
from pymez.http import Http
import json


class Account(object):
    '''
    Representation of account information for the owner of this account
    '''

    def __init__(self,
                 url,
                 userid,
                 passwd,
                 headers={}):
        '''
        Initialize
        '''

        self.headers = headers
        self.headers['Accept'] = ACCOUNT_INFO
        self.passwd = passwd
        self.url = url
        self.userid = userid
        self.http = Http(self.url,
                         headers=self.headers)
        self._get()

    def _get(self):
        '''
        Get the account information.
        '''
        status, content, _headers = self.http.GET()
        if not status in [200]:
            return None
        self._account_info = json.loads(content)
        self._account_type = \
            self._account_info['account-info']['account_type']
        self._allocated_bandwidth = \
            self._account_info['account-info']['bandwidth']['allocated']
        self._private_bandwidth = \
            self._account_info['account-info']['bandwidth']['private']
        self._public_bandwidth = \
            self._account_info['account-info']['bandwidth']['public']
        self._total_bandwidth = \
            self._account_info['account-info']['bandwidth']['total']
        self._mgmt_uri = \
            self._account_info['account-info']['mgmt_uri']
        self._s3_auth_id = \
            self._account_info['account-info']['s3_auth_id']
        self._s3_auth_key = \
            self._account_info['account-info']['s3_auth_key']
        self._allocated_storage = \
            self._account_info['account-info']['storage']['allocated']
        self._storage_used = \
            self._account_info['account-info']['storage']['used']
        self._username = \
            self._account_info['account-info']['username']

    def GET(self):
        '''
        Return the account information as a dictionary.
        '''
        return self._account_info

    def get_account_type(self):
        return self._account_type

    def get_allocated_bandwidth(self):
        return self._allocated_bandwidth

    def get_private_bandwidth(self):
        return self._private_bandwidth

    def get_public_bandwidth(self):
        return self._public_bandwidth

    def get_total_bandwidth(self):
        return self._total_bandwidth

    def get_management_uri(self):
        return self._mgmt_uri

    def get_s3_auth_id(self):
        return self._s3_auth_id

    def get_s3_auth_key(self):
        return self._s3_auth_key

    def get_allocated_storage(self):
        return self._allocated_storage

    def get_storage_used(self):
        return self._storage_used

    def get_username(self):
        return self._username
