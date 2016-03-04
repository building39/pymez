#!/usr/bin/python
# encoding: utf-8
'''
cr -- shortdesc

cr is a description

It defines classes_and_methods

@author:     John Thornton

@copyright:  2013 Klink LLC. All rights reserved.

@license:    All rights reserved by Klink LLC

@contact:    john@klinkcdc.com
@deffield    updated: Updated
'''

import sys
import os
import requests
try:
    from local_utils.find_user import find_user
    GDL_AVAILABLE = True
except:
    GDL_AVAILABLE = False

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter


__all__ = []
__version__ = 0.1
__date__ = '2013-09-27'
__updated__ = '2014-02-05'


def main(argv=None):

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = 'Klink'
    program_license = '''%s

  Copyright 2013 Klink LLC. All rights reserved.

USAGE
''' % program_shortdesc

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-e", "--env", dest="env", default='dev1',
                            help="the environment dev1|test|stage|prod")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count",
                            help="set verbosity level [default: %(default)s]")
        parser.add_argument('user', nargs='+', help="a email address, phone number, or gdl uuid")
        # Process arguments
        args = parser.parse_args()
        app_env = args.env
        user = args.user[0]
        print get_creds(user, app_env)
    except KeyboardInterrupt:
        return 0
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

def set_env(app_env):
    if app_env == 'prod':
        gdl_base_url = 'https://api-private.ena.groupdigitallife.net/'
        _app_base_url = 'https://files.klink.com/'
        gdl_client_id = 'safecloud'
        gdl_client_secret = 'd94f1c0a2148d6ea8e652859b947dad8'

    elif app_env == 'stage':
        gdl_base_url = 'https://api-private.sandbox.ena.groupdigitallife.net/'
        _app_base_url = 'https://files-stage.klink.com/'
        gdl_client_id = 'safecloud'
        gdl_client_secret = 'd18cce1b295517decf46a680f5b8cb08'

    elif app_env == 'test':
        gdl_base_url = 'https://api-private.sandbox.ena.groupdigitallife.net/'
        _app_base_url = 'https://files-test.klink.com/'
        gdl_client_id = 'safecloud'
        gdl_client_secret = 'd18cce1b295517decf46a680f5b8cb08'
    elif app_env == 'dev1':
        gdl_base_url = 'https://api-private.sandbox.ena.groupdigitallife.net/'
        _app_base_url = 'https://files-dev1.klink.com/'
        gdl_client_id = 'safecloud'
        gdl_client_secret = 'd18cce1b295517decf46a680f5b8cb08'
    elif app_env == 'dev4' or app_env == 'uat':
        gdl_base_url = 'https://api-private.sandbox.ena.groupdigitallife.net/'
        _app_base_url = 'https://files-dev4.klink.com/'
        gdl_client_id = 'safecloud'
        gdl_client_secret = 'd18cce1b295517decf46a680f5b8cb08'

        return (gdl_base_url, gdl_client_id, gdl_client_secret)

def get_creds(user_id, app_env):
    
    if not GDL_AVAILABLE:
        print 'GDL is not available in this environment.'
        return ('', 501, 'Not Implemented')

    gdl_base_url, gdl_client_id, gdl_client_secret = set_env(app_env)

    url = gdl_base_url + 'v1/token/access_trusted'

    params = {'user_id': user_id}
    params['client_id'] = gdl_client_id
    params['client_secret'] = gdl_client_secret
    params['grant_type'] = 'urn:gdl:trusted'
    params['scope'] = 'sso profile'


    headers = {"X-PARTNER-ID": "e391312d-d492-4c13-9466-dad0ae1c1ad2", "accept-type": "application/json"}

    results = requests.post(url=url, params=params, headers=headers)
    if results.status_code != 200:
        print'failed to get trusted token with reason :' + str(results.status_code)
        return (None, results.status_code, results.data)

    return  (results.json()['access_token'], results.status_code, results.text)


if __name__ == "__main__":
    sys.exit(main())
