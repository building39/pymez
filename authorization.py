'''
Created on Geb 11, 2014

@author: mmartin
'''

from base64 import encodestring
from pymez.get_creds import get_creds

import sys


class Authorization(object):
    '''
    Do authorization.
    '''

    def __init__(self,
                 userid,
                 gdl_env=None,
                 passwd=None):

        if gdl_env:
            if gdl_env in ['dev1', 'dev4', 'test', 'stage', 'prod']:
                self.auth = self._gdl_auth(userid, gdl_env)
            else:
                # TODO: throw an error here
                self.auth = 'invalid gdl env %s' % gdl_env
                sys.exit(1)
        else:
            self.auth = self._basic_auth(userid, passwd)

    def get_auth(self):
        return self.auth


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
