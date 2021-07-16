#TODO: mkdir csv if it does not exist. If it exists then rm csv/*


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

#fields contains the keys in json file which will be extracted
fields = ["timestamp","tx_id","Mspid", "activity_name", "function_args", "endorsers_id", "tx_status", "readkeys", "writekeys", "rangekeys", "transaction_type", "case_id"]

home_dir = "/home/ubuntu/BlockProM/log_store/"
log_dir = ' '.join(sys.argv[1:])
full_path = home_dir + log_dir + "/csv"

#csv_path is the path to the output file, in which the extracted data is written in csv format
csv_path =full_path + "/clean_blockchainlog.csv"


file_dir=home_dir + log_dir

writer = csv.writer(open('%s/metrics.csv' % full_path, 'w'))
writer.writerow(["Metrics", "Variable_Name","Value"])

file = open(csv_path)
reader = csv.reader((x.replace('\0', '') for x in file), delimiter=',')
new_lines = list(reader)

n=0
TM=0

optcount = 0

def is_phrase_in(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None

def __datetime(date_str):
    return datetime.strptime(date_str, '%a-%b-%d%T%H:%M:%S%Z')
    #2021-07-13T10:19:51.987Z

def rate_metrics():
    #Total number of transactions in the log
    global n 
    global new_lines
    n = len(new_lines) - 1
    start = arrow.get(new_lines[1][0]).datetime
    end = arrow.get(new_lines[n][0]).datetime
    #Total time taken for n transactions
    global TM 
    TM = (end - start).total_seconds()
    #Transaction rate
    Tr = n/TM
    #global writer
    writer.writerow(["Total number of transactions", "n",str(n)])
    writer.writerow(["Transaction rate", "Tr",str(Tr)])

def failure_metrics():

    global n
    global TM
    global new_lines
    nf = 0
    nMRC = 0
    nEPF = 0
    nPRC = 0
    for i in range(len(new_lines)):
        if new_lines[i][6] != "VALID":
            nf += 1
            if new_lines[i][6] == "MVCC_READ_CONFLICT":
                nMRC += 1
            elif new_lines[i][6] == "ENDORSEMENT_POLICY_FAILURE":
                nEPF += 1
            elif new_lines[i][6] == "PHANTOM_READ_CONFLICT":
                nPRC += 1


    writer.writerow(["Total Failure", "TF",str(nf)])
    writer.writerow(["Total Failure rate", "TFr",str(nf/TM)])
    writer.writerow(["Total Failure %", "TFp",str((nf/n)*100)])
    writer.writerow(["MVCC read conflict", "MRC",str(nMRC)])
    writer.writerow(["MVCC read conflict rate", "MRCr",str(nMRC/TM)])
    writer.writerow(["MVCC read conflict %", "MRCp",str((nMRC/n)*100)])
    writer.writerow(["Endorsement policy failure", "EPF",str(nEPF)])
    writer.writerow(["Endorsement policy failure rate", "EPFr",str(nEPF/TM)])
    writer.writerow(["Endorsement policy failure %", "EPFp",str((nEPF/n)*100)])
    writer.writerow(["Phantom read conflict", "PRC",str(nPRC)])
    writer.writerow(["Phantom read conflict rate", "PRCr",str(nPRC/TM)])
    writer.writerow(["Phantom read conflict %", "PRCp",str((nPRC/n)*100)])


def originator_sig():

    global new_lines
    writer = csv.writer(open('%s/originator_significance.csv' % full_path, 'w'))
    writer.writerow(["Originator", "OGsig"])
    clients=[]
    for i in range(len(new_lines)):
        if i != 0 and new_lines[i][2] not in clients:
           clients.append(new_lines[i][2])

    ogrows = [[None for _ in range(2)] for _ in range(len(clients))]

    for k in range(len(clients)):
        txcount = 0
        for i in range(len(new_lines)):
            if i != 0 and new_lines[i][2]==clients[k]:
               txcount+=1
        ogrows[k] = [clients[k], txcount]

    ogrows_sort = sorted(ogrows,key=lambda l:l[1], reverse=True)
    writer.writerows(ogrows_sort)

def endorser_sig():

    global new_lines
    writer = csv.writer(open('%s/endorser_significance.csv' % full_path, 'w'))
    writer.writerow(["Endorser", "EDsig"])
    endorsers=[]
    for i in range(len(new_lines)):
        if i != 0 and new_lines[i][5] not in endorsers:
           endorsers.append(new_lines[i][5])

    edrows = [[None for _ in range(2)] for _ in range(len(endorsers))]

    for k in range(len(endorsers)):
        txcount = 0
        for i in range(len(new_lines)):
            if i != 0 and new_lines[i][5]==endorsers[k]:
               txcount+=1
        edrows[k] = [endorsers[k], txcount]

    edrows_sort = sorted(edrows,key=lambda l:l[1], reverse=True)
    writer.writerows(edrows_sort)



def key_sig():
    writer = csv.writer(open('%s/key_significance.csv' % full_path, 'w'))
    writer.writerow(['Keys','Ksig','activity_names'])
    unique_keys=[]
    for i in range(len(new_lines)):
        readkey = []
        writekey = []
        rangekey = []
        if i != 0 :
           readkey += (new_lines[i][7].strip()).split()
           for k in readkey:
             if k not in unique_keys and k != 'NULL' and k != '':
                unique_keys.append(k)
           writekey += (new_lines[i][8].strip()).split()
           for k in writekey:
             if k not in unique_keys and k != 'NULL' and k != '':
                unique_keys.append(k)
           rangekey += (new_lines[i][9].strip()).split()
           for k in rangekey:
             if k not in unique_keys and k != 'NULL' and k != '':
                unique_keys.append(k)

    key_dependencies=[]
    for key in unique_keys:
        numdependencies=0
        activity_names=''

        for i in range(len(new_lines)):
            if i != 0 :
               if (key != '') and (is_phrase_in(key, new_lines[i][7].strip()) or is_phrase_in(key, new_lines[i][8].strip()) or is_phrase_in(key, new_lines[i][9].strip())):
                   numdependencies+=1
                   activity_names = activity_names + ' ' + new_lines[i][3]
        key_dependencies.append([key,numdependencies,activity_names]) 
    key_dependencies_sort = sorted(key_dependencies,key=lambda l:l[1], reverse=True)
    writer.writerows(key_dependencies_sort)

def datavalue_correlation():
    writer = csv.writer(open('%s/datavalue_correlation.csv' % full_path, 'w'))
    writer.writerow(['Failed transaction','activity_name','Readset','WriteSet','RangeReadSet','Dependent transaction(valid)','activity_name','Readset','WriteSet','RangeReadSet','ReorderingPossibility'])
    
    dv=[]

    for i in range(len(new_lines)):
        if (new_lines[i][6] == "MVCC_READ_CONFLICT" or new_lines[i][6] == "PHANTOM_READ_CONFLICT"):
            for j in range(i-1, 0, -1):
                txstatus = new_lines[j][6]
                readseti = set(new_lines[i][7].split())
                writeseti = set(new_lines[i][8].split())
                rangeseti = set(new_lines[i][9].split())
                writesetj = set(new_lines[j][8].split())
                if ((txstatus == "VALID") and ((readseti != '') or (rangeseti != '')) and ((bool(readseti.intersection(writesetj)) == True) or (bool(rangeseti.intersection(writesetj)) == True))):
                    if (bool(writeseti.intersection(writesetj)) == False):
                        reorder = True
                    else:
                        reorder = False

                    dv.append([new_lines[i][1],new_lines[i][3],new_lines[i][7],new_lines[i][8],new_lines[i][9],new_lines[j][1],new_lines[j][3],new_lines[j][7],new_lines[j][8],new_lines[j][9],reorder])

    writer.writerows(dv)


def client_dist():
    global n
    global optcount
    cpath = full_path + '/originator_significance.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)
    nclients = len(cnew_lines) - 1
    ct1 = n // 2
    ct2 = nclients // 2
    ntx = 0
    clients=[]

    for i in range(1, ct2+1):
        ntx += int(cnew_lines[i][1])
        clients.append(cnew_lines[i][0])
    if ntx > ct1:
        optcount += 1
        print()
        print(optcount, "Optimization recommendation: Redistribute clients because client bottleneck was detected")
        print(ntx," transactions out of", n," transactions were send by the clients:", clients)
        print()
        print("##########################################################################################")
    

def endorser_dist():
    global n
    global optcount
    cpath = full_path + '/endorser_significance.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)
    nendorsers = len(cnew_lines) - 1
    et1 = n // 2
    et2 = nendorsers // 2
    ntx = 0
    endorsers=[]

    for i in range(1, et2+1):
        ntx += int(cnew_lines[i][1])
        endorsers.append(cnew_lines[i][0])
    if ntx > et1:
        optcount += 1
        print()
        print(optcount, "Optimization recommendation: Redefined endorsement policy because endorser bottleneck was detected")
        print(ntx," transactions out of", n," transactions were send by the set of endorsers:", endorsers)
        print()
        print("##########################################################################################")

def read_tx_batch():
    global n
    global new_lines
    global optcount
    nRT = 0
    nfRT = 0
    rt_fail_tx = []

    for i in range(len(new_lines)):
        if new_lines[i][10] == "RT" or new_lines[i][10] == "RRT":
            nRT += 1

    for i in range(len(new_lines)):
        if ((new_lines[i][6] == "MVCC_READ_CONFLICT" or new_lines[i][6] == "PHANTOM_READ_CONFLICT") and (new_lines[i][10] == "RT" or new_lines[i][10] == "RRT")):
            nfRT += 1
            rt_fail_tx.append(new_lines[i][3])


    bat=nRT/2

    #print(nRT)
    #print(nfRT)
    #print(rt_fail_tx)

    if nfRT > bat:
        optcount += 1
        print()
        print(optcount, "Optimization recommendation: Batch read transactions")
        print(nfRT," transactions out of",nRT," read transactions failed due to read conflicts. The failed transactions are:", rt_fail_tx)
        print()
        print("##########################################################################################")

def tx_reordering():
    global n
    global new_lines
    global optcount
    cpath = full_path + '/datavalue_correlation.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)
    reorderpairs=[]
    reorderpairs_inv=[]
    index=[]
    for i in range(len(cnew_lines)):
        if ((i != 0) and (cnew_lines[i][10]) and (cnew_lines[i][1] != cnew_lines[i][6])):
            reorderpairs.append([cnew_lines[i][6], cnew_lines[i][1]])
            reorderpairs_inv.append([cnew_lines[i][1], cnew_lines[i][6]])

    #print(set(reorderpairs_inv).intersection(set(reorderpairs)))
    for i in range(len(reorderpairs)):
        for j in range(len(reorderpairs_inv)):
            if (reorderpairs[i] == reorderpairs_inv[j]):
                index.append(i)
                break

    #print(reorderpairs)
    #print(index)
    dynamicindex=0
    for i in range(len(index)):
        if i == 0:
            reorderpairs.remove(reorderpairs[index[i]])
            dynamicindex += 1
        else:
            reorderpairs.remove(reorderpairs[index[i]-dynamicindex])
            dynamicindex += 1

    #print(reorderpairs)
    reorderpairs_final=set(tuple(element) for element in reorderpairs)
    counts = Counter(map(tuple, reorderpairs))


    if (len(reorderpairs) > 0):
        optcount += 1
        print()
        print(optcount, "Optimization recommendation: Reordering possibilities detected")
        print("The following pairs of transactions can be reordered (reverse the order) to avoid conflicts:")
        print(reorderpairs_final)
        print("The number of conflicts for each pair is as follows:")
        print(counts)
        print()
        print("##########################################################################################")


def deltawrites():
    global n
    global new_lines
    global optcount
    cpath = full_path + '/datavalue_correlation.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)

    deltatx=[]
    for i in range(len(cnew_lines)):
        if ((i != 0) and len(cnew_lines[i][8].split()) == 1):
            deltatx.append(cnew_lines[i][6])

    deltatx_final=set(deltatx)
    counts = Counter(deltatx)

    if (len(deltatx) > 0):
        optcount += 1
        print()
        print(optcount, "Optimization recommendation: Possibility of delta writes detected")
        print("The following transactions contain writes to a single key and could be converted to delta writes to avoid conflicts:")
        print(deltatx_final)
        print("The number of conflicts caused by each transaction is as follows:")
        print(counts)
        print()
        print("##########################################################################################")

def splitbatch_chaincodes():
    global optcount
    cpath = full_path + '/key_significance.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)

    ht1 = 3
    if (len(cnew_lines) > 1):
        optcount += 1
        print()
        print(optcount, "Optimization recommendation: Hot keys have been detected")
        print("The top", ht1, "hotkeys are shown below along with the transactions that use them.")
        print("Spliting chaincodes or batching withing the chaincodes are possible optimizations to avoid conflicts:")
        print()
    for i in range(1, ht1+1):
        txnames=set(cnew_lines[i][2].split())
        print(i, "Key:", cnew_lines[i][0], "Frequency:", cnew_lines[i][1], "Transactions:", txnames)

    print()
    print("##########################################################################################")

#Metrics
rate_metrics()
failure_metrics()
originator_sig()
endorser_sig()
key_sig()
datavalue_correlation()

#Optimization strategies
client_dist()
endorser_dist()
#blocksize_opt()
read_tx_batch()
#load_shedding()
tx_reordering()
deltawrites()
splitbatch_chaincodes()


