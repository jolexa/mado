#!/usr/bin/env python

import os
import time
import requests
import json

def do_scaling(value):
    if value > os.environ.get('THRESHOLD'):
        print "Scaling Up.."
        factor = "1." + os.environ.get("SCALE_UP_PERCENT")
        body = json.dumps({u"scaleBy": float(factor)})
    elif value < os.environ.get('THRESHOLD'):
        print "Scaling Down.."
        # The really, really nice thing about using percentages is that marathon
        # will never round down, only up. So, for example, starting at 100 and
        # scaling down by 80% will eventually converge at 4, not going below.
        # Every percentage has a number it will converge to. 10% -> 9, etc
        factor = "0." + os.environ.get("SCALE_DOWN_PERCENT")
        body = json.dumps({u"scaleBy": float(factor)})
    else:
        print "No Change"

    uri = "http://marathon.mesos:8080/v2/groups/" + os.environ.get('MARATHON_APP_GROUP')
    if body:
        print "DEBUG: Calling: {0}, with payload: {1}".format(uri, body)
        r = requests.put(uri, data=body )
        print r.text

if os.environ.get('POLL_SERVICE') == "logicmonitor":
    LM_COMPANY = os.environ.get('LM_COMPANY')
    LM_USER = os.environ.get('LM_USER')
    LM_PASS = os.environ.get('LM_PASS')
    LM_HOST = os.environ.get('LM_HOST')
    LM_DATASOURCE = os.environ.get('LM_DATASOURCE')
    LM_DATAPOINT = os.environ.get('LM_DATAPOINT')
    epoch = int(time.time())

    payload = {'c': LM_COMPANY, 'u': LM_USER, 'p': LM_PASS, 'host': LM_HOST,
        'dataSource': LM_DATASOURCE, 'dataPoint0': LM_DATAPOINT,
        'start': epoch - 180, 'end': epoch }
    uri = "https://" + LM_COMPANY + ".logicmonitor.com/santaba/rpc/getData"
    r = requests.get(uri, params=payload)

    totalvalue = 0
    value = 0
    for dp in r.json()["data"]["values"][LM_DATASOURCE]:
        epoch = dp[0]
        humantime = dp[1]
        if dp[2] != "NaN":
            value = dp[2]
            totalvalue += value
    print "DEBUG: there is a cumulative queuedepth of: {0}, past 3 minutes".format(totalvalue)

    do_scaling(totalvalue)


else:
    print "POLL_SERVICE is not supported yet"
