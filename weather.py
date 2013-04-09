#! /usr/bin/env python

import os
import sys
import json
import urllib2

zipcodes=sys.argv[1]
zipcodes = zipcodes.split(',')
ff=open('file','w+')

for z in zipcodes:
    urllocation = 'http://api.wunderground.com/api/eefb43bdb7e835d5/hourly/q/'+str(z)+'.json'
    print 'Processing ' + urllocation
    f = urllib2.urlopen(urllocation)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    if 'hourly_forecast' in parsed_json.keys():
        for i in range(4):
            forecast, weekday,temp,condition = parsed_json['hourly_forecast'][i]['FCTTIME']['pretty'], parsed_json['hourly_forecast'][i]['FCTTIME']['weekday_name'],parsed_json['hourly_forecast'][i]['temp']['english'],parsed_json['hourly_forecast'][i]['condition']
            # Store in a file
            res = (str(str(z)+'>>'+forecast+'|'+ weekday+'|'+str(temp)+'|'+condition+'\n'))
            ff.write(res)
            print res
ff.close()

