#!/usr/bin/env python

import os
import time
import json
from datetime import timedelta
from datetime import datetime
import requests

def get_current_count_by_group(group):
    # This is an rough science, as we are checking for the entire group, not an
    # individual application
    uri = "http://marathon.mesos:8080/v2/groups/" + os.environ.get('MARATHON_APP_GROUP')
    r = requests.get(uri)
    instances = 0
    for app in r.json()["apps"]:
        instances += app["instances"]
    return instances

def do_scaling(value):
    try:
        FLOOR = os.environ["SCALE_FLOOR"]
    except KeyError:
        FLOOR = False
    try:
        CEILING = os.environ["SCALE_CEILING"]
    except KeyError:
        CEILING = False

    if value > os.environ.get('THRESHOLD'):
        if CEILING:
            if CEILING > get_current_count_by_group(os.environ.get('MARATHON_APP_GROUP')):
                print "SCALE_CEILING is not met. Scaling Up.."
                factor = "1." + os.environ.get("SCALE_UP_PERCENT")
                body = json.dumps({u"scaleBy": float(factor)})
            else:
                print "CEILING is already met, not proceeding"
        else:
            print "SCALE_CEILING is not set, so scaling up. Potential runaway scaling possibility."
            factor = "1." + os.environ.get("SCALE_UP_PERCENT")
            body = json.dumps({u"scaleBy": float(factor)})

    elif value < os.environ.get('THRESHOLD'):
        # The really, really nice thing about using percentages is that marathon
        # will never round down, only up. So, for example, starting at 100 and
        # scaling down by 80% will eventually converge at 4, not going below.
        # Every percentage has a number it will converge to. 10% -> 9, etc
        if FLOOR:
            if FLOOR < get_current_count_by_group(os.environ.get('MARATHON_APP_GROUP')):
                print "SCALE_FLOOR is not met. Scaling Down.."
                factor = "0." + str(100 - int(os.environ.get("SCALE_DOWN_PERCENT")))
                body = json.dumps({u"scaleBy": float(factor)})
            else:
                print "FLOOR is already met, not proceeding"
        else:
            print "SCALE_FLOOR is not set, so scaling down. Potential to be below desired capacity."
            factor = "0." + os.environ.get("SCALE_DOWN_PERCENT")
            body = json.dumps({u"scaleBy": float(factor)})
    else:
        print "No Change"

    uri = "http://marathon.mesos:8080/v2/groups/" + os.environ.get('MARATHON_APP_GROUP')
    if body:
        print "DEBUG: Calling: {0}, with payload: {1}".format(uri, body)
        r = requests.put(uri, data=body)
        print r.text

if os.environ.get('BACKEND_SERVICE') == "logicmonitor":
    LM_COMPANY = os.environ.get('LM_COMPANY')
    LM_USER = os.environ.get('LM_USER')
    LM_PASS = os.environ.get('LM_PASS')
    LM_HOST = os.environ.get('LM_HOST')
    LM_DATASOURCE = os.environ.get('LM_DATASOURCE')
    LM_DATAPOINT = os.environ.get('LM_DATAPOINT')
    epoch = int(time.time())

    payload = {'c': LM_COMPANY, 'u': LM_USER, 'p': LM_PASS, 'host': LM_HOST,
               'dataSource': LM_DATASOURCE, 'dataPoint0': LM_DATAPOINT,
               'start': epoch - 180, 'end': epoch
              }
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
    print "DEBUG: Over the past 3 minutes, the datapoint, {1}, has added up to: {0}".format(totalvalue, LM_DATAPOINT)
    do_scaling(totalvalue)

elif os.environ.get('BACKEND_SERVICE') == "cloudwatch":
    import boto3
    client = boto3.client('cloudwatch')

    AG_TYPE = os.environ.get('CW_AGGREGATION_TYPE')
    response = client.get_metric_statistics(
        Namespace=os.environ.get('CW_NAMESPACE'),
        MetricName=os.environ.get('CW_METRIC'),
        StartTime=datetime.utcnow() - timedelta(minutes=3),
        EndTime=datetime.utcnow(),
        Period=60,
        Statistics=[AG_TYPE],
        Dimensions=[
            {'Name': os.environ.get('CW_DIMENSION_NAME'), 'Value': os.environ.get('CW_DIMENSION_VALUE')}
        ])
    value = float(0)
    total = float(0)
    counter = 0
    skip = False
    if not response["Datapoints"]:
        print "No Data to work on"
        skip = True
    for i in response["Datapoints"]:
        counter += 1
        print "DEBUG: Iterating on value: " + str(i[AG_TYPE])
        if AG_TYPE == "Maximum":
            value += i[AG_TYPE]
        elif AG_TYPE == "Average":
            total += i[AG_TYPE]
            value = total / counter
    print "DEBUG: Type: {0}, is value: {1}".format(AG_TYPE, value)
    if not skip:
        do_scaling(value)

else:
    print "BACKEND_SERVICE is not supported yet"
