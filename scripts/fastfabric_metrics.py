

#!/usr/bin/env python

import json
import os
import collections
import re
import csv
import sys
from datetime import datetime, date
import arrow
from collections import Counter
#the extract function is used from: 
#https://hackersandslackers.com/extract-data-from-complex-json-python/

def is_phrase_in(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None

def __datetime(date_str):
    return datetime.strptime(date_str, '%a-%b-%d%T%H:%M:%S%Z')
    #2021-07-13T10:19:51.987Z

def rate_metrics():

    #Blocksize40
    #n = 1250
    #timestamp1 = "2022-04-01T09:01:21.845Z"
    #timestamp2 = "2022-04-01T09:01:24.636Z"
    #Blocksize100
    #n = 400 
    #timestamp1 = "2022-04-01T10:10:05.654Z"
    #timestamp2 = "2022-04-01T10:10:06.778Z"
    #Blocksize100 clients 10
    n = 202
    timestamp1 = "2022-04-01T13:48:25.143Z"
    timestamp2 = "2022-04-01T13:48:26.441Z"
    totalfails = 131
    failpercent = 63.28502415458937
    start = arrow.get(timestamp1).datetime
    end = arrow.get(timestamp2).datetime
    TM = (end - start).total_seconds()
    Tr = n/TM
    latency = TM/n
    succthroughput = (n - totalfails)/TM
    succpercent = 100 - failpercent

    print("succthroughput")
    print(succthroughput)
    print("Latency")
    print(latency)
    print("succpercent")
    print(succpercent)
    print("Duration")
    print(TM)
    print("Throughput")
    print(Tr)

rate_metrics()


