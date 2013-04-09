#!/usr/bin/python
# coding: utf-8

import facebook
import urllib
import urlparse
import subprocess
import warnings
import os
import sys
import json


brands = sys.argv[1]
brands = brands.split(',')
filename = brands[0]
brands = brands[1:]

ff=open(filename,'w+')
for b in brands:
    # Hide deprecation warnings. The facebook module isn't that up-to-date (facebook.GraphAPIError).
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    # Parameters of your app and the id of the profile you want to mess with.
    FACEBOOK_APP_ID     = '200697930054944'
    FACEBOOK_APP_SECRET = 'e10801aaa78a79fc6e9c4633a5d187ab'
    FACEBOOK_PROFILE_ID = str(b)
    print b

    # Trying to get an access token. Very awkward.
    oauth_args = dict(client_id     = FACEBOOK_APP_ID,
                  client_secret = FACEBOOK_APP_SECRET,
                  grant_type    = 'client_credentials')
    oauth_curl_cmd = ['curl',
                  'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]


    oauth_response = subprocess.Popen(oauth_curl_cmd,
                                  stdout = subprocess.PIPE,
                                  stderr = subprocess.PIPE).communicate()[0]

    try:
        oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
    except KeyError:
        print('Unable to grab an access token!')
        exit()

    graph = facebook.GraphAPI(oauth_access_token)
    #Printing own info
    user = graph.get_object(FACEBOOK_PROFILE_ID)

    # Retreving likes and name
    likes=user['likes']
    name=user['name']
    result= name+'\t'+str(likes)
    ff.write(result)
ff.close()
