

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

home_dir = "/home/ubuntu/BlockProM/log_store/"
#log_dir = ' '.join(sys.argv[1:])
log_dir = str(sys.argv[1])
#exp_num = ' '.join(sys.argv[2:])
exp_num = str(sys.argv[2])
full_path = home_dir + log_dir + "/csv"

def extractcaliperlogs():
    nwriter = csv.writer(open('%s/allmetricslog.csv' % home_dir, 'a'))
    writer = csv.writer(open('%s/metricslog.csv' % full_path, 'w'))
    writer.writerow(["ExpNum", "Succ", "Fail","SendRate","Latency","Throughput","Duration","SuccThroughput","SuccRate"])

    cpath = full_path + '/tempmetricslog.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)

    succ=float(cnew_lines[0][0])+float(cnew_lines[0][1])
    fail=float(cnew_lines[0][2])+float(cnew_lines[0][3])
    sendrate=(float(cnew_lines[0][4])+float(cnew_lines[0][5]))/2
    latency=(float(cnew_lines[0][6])+float(cnew_lines[0][7]))/2
    throughput=(float(cnew_lines[0][8])+float(cnew_lines[0][9]))/2
    duration=(succ+fail)/throughput
    succthroughput=succ/duration
    succrate=(succ/(succ+fail))*100

    writer.writerow([exp_num,succ,fail,sendrate,latency,throughput,duration,succthroughput,succrate])
    nwriter.writerow([exp_num,succ,fail,sendrate,latency,throughput,duration,succthroughput,succrate])


extractcaliperlogs()

