#!/usr/bin/env python
'''
Created on Mar 24, 2013

@author: mmartin
'''
import getpass
from pymez.cloud import Cloud

import sys
import time

URL = 'www.fuzzcat.net'
USERID = 'mmartin'

cloud = None


def do_get_account():
    account_info = cloud.get_account()
    print 'Account info:'
    print '    Account Type:   %s' % account_info.get_account_type()
    print '    Bandwidth:'
    print '        Allocated:  %d' % account_info.get_allocated_bandwidth()
    print '        Private:    %d' % account_info.get_private_bandwidth()
    print '        Public:     %d' % account_info.get_public_bandwidth()
    print '        Total:      %d' % account_info.get_total_bandwidth()
    print '    Management URI: %s' % account_info.get_management_uri()
    print '    S3 Auth ID:     %s' % account_info.get_s3_auth_id()
    print '    S3 Auth Key:    %s' % account_info.get_s3_auth_key()
    print '    Storage:'
    print '        Allocated:  %d' % account_info.get_allocated_storage()
    print '        Used:       %d' % account_info.get_storage_used()
    print '    User Name:      %s' % account_info.get_username()


def do_get_cloud():
    print 'Cloud info:'
    print '    Account URI:        %s' % cloud.get_account_uri()
    print '    Allspaces URI:      %s' % cloud.get_allspaces_uri()
    print '    Locations:'
    num_locs = cloud.how_many_locations()
    for location in range(num_locs):
        print '    Location #%d:' % num_locs
        print ('        Default:        %s' %
               cloud.is_location_default(location))
        print ('        Mgmt URI:       %s' %
               cloud.get_location_mgmt_uri(location))
        print ('        Name:           %s' %
               cloud.get_location_name(location))
        print ('        Namespace:      %s' %
               cloud.get_location_namespace_uri(location))
        print ('        Notifications:  %s' %
               cloud.get_location_notifications_uri(location))
        print ('        Root Container: %s' %
               cloud.get_location_root_container_uri(location))
        print ('        Spaces:         %s' %
               cloud.get_location_spaces_uri(location))
    print '    Namespaces URI:     %s' % cloud.get_namespaces_uri()
    print '    Recycle bin URI:    %s' % cloud.get_recyclebin_uri()
    print '    Search URI:         %s' % cloud.get_search_uri()
    print '    Shares URI:         %s' % cloud.get_shares_uri()
    print '    Tags URI:           %s' % cloud.get_tags_uri()


def do_get_locations():
    locations = cloud.get_locations()
    container_number = 0
    for location in locations:
        rootContainer = location.get_root_container()
        container_number += 1
        print_container(rootContainer, container_number)


def print_container(container, which):
    print 'Container %s' % container
    print '    Root Container #%d:' % which
    print '        Name:          %s' % container.get_name()
    print '        Date Created:  %s' % time.ctime(container.get_created())
    print '        Last Accessed: %s' % time.ctime(container.get_accessed())
    print '        Last Modified: %s' % time.ctime(container.get_modified())
    print '        Modified By:   %s' % container.get_modified_by()
    print '        Bytes:         %d' % container.get_bytes()
    print '        Shared:        %s' % container.get_shared()
    print '        Owner:         %s' % container.get_owner()
    print '        Version:       %s' % container.get_version()
    print '        Comments:      %s' % container.get_comments()
    print '        Contents:      %s' % container.get_contents()
    print '        Metadata:      %s' % container.get_metadata()
    print '        Notifications: %s' % container.get_notifications()
    print '        Permissions:   %s' % container.get_permissions()
    print '            Principal: %s' % container.get_principal()
    print '            Simple:    %s' % container.get_simple()
    print '        Tags:          %s' % container.get_tags()
    print '        Uri:           %s' % container.get_uri()
    print '        Parent:        %s' % container.get_parent()


def usage():
        print 'Usage: %s <password>' % sys.argv[0]
        sys.exit(1)


def main(argv):
        if (len(sys.argv) < 2):
                usage()
        global cloud
        cloud = Cloud(USERID, getpass.getpass(), URL)  # get the cloud object
        do_get_cloud()  # print cloud information
        do_get_account()  # print account information
        do_get_locations()
        cloud.close()  # close the connection pool

if __name__ == '__main__':
    main(sys.argv[1:])
