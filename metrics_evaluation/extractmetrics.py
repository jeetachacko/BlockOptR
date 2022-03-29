

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
log_dir = str(sys.argv[1])
exp_num = str(sys.argv[2])
full_path = home_dir + log_dir + "/csv"

def extractlogs():
    mpath = full_path + '/failuremetrics.csv'
    mfile = open(mpath)
    mreader = csv.reader((x.replace('\0', '') for x in mfile), delimiter=',')
    mnew_lines = list(mreader)

    writer = csv.writer(open('%s/blockchainallmetricslog.csv' % full_path, 'w'))
    writer.writerow(["ExpNum", "SendRate","Latency","Throughput","Duration","TotalNumTxs","Succ","SuccThroughput","SuccPercent","Fail","FailPercent","Mvcc","EndorseFail","PhantomReads"])

    cpath = full_path + '/tempmetricslog.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)

    #succ=float(cnew_lines[0][0])+float(cnew_lines[0][1])
    #fail=float(cnew_lines[0][2])+float(cnew_lines[0][3])
    sendrate=(float(cnew_lines[0][4])+float(cnew_lines[0][5]))/2
    latency=(float(cnew_lines[0][6])+float(cnew_lines[0][7]))/2
    throughput=(float(cnew_lines[0][8])+float(cnew_lines[0][9]))/2
    #duration=(succ+fail)/throughput
    #succthroughput=succ/duration
    #succrate=(succ/(succ+fail))*100

    totalfailures=float(mnew_lines[1][2])
    failrate=float(mnew_lines[2][2])
    failpercent=float(mnew_lines[3][2])
    totalmvcc=float(mnew_lines[4][2])
    totalendf=float(mnew_lines[7][2])
    totalphantom=float(mnew_lines[10][2])
    totaltx=(totalfailures*100)/failpercent
    totalsucc=totaltx-totalfailures
    succpercent=(totalsucc/totaltx)*100
    duration=(totalsucc+totalfailures)/throughput
    succthroughput=totalsucc/duration

    writer.writerow([exp_num,sendrate,latency,throughput,duration,totaltx,totalsucc,succthroughput,succpercent,totalfailures,failpercent,totalmvcc,totalendf,totalphantom])

extractlogs()

