#! /usr/bin/python
import sys
import twitter

api = twitter.Api(consumer_key='',
consumer_secret='', access_token_key='', access_token_secret='')
api.VerifyCredentials()

keys = keys.split(',')
filename = keys[0]
apitype = keys[1]
keys = keys[2:]

print filename,apitype,keys

ff = open(filename,'w+')
for k in keys:
    if apitype == 'search':
        t = api.GetSearch(k)
        for a in t:
            result =  a.text.encode('utf-8').strip()
            ff.write(result)
    elif apitype == 'timeline':
        t = api.GetSearch()
        for a in t:
            result =  a.text.encode('utf-8').strip()
            ff.write(result)
    else:
        result = sprintf("API %s is not defined",apitype)
        ff.write(result)
    
ff.close()
