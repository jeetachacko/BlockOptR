

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
fields = ["timestamp","tx_id","Mspid", "activity_name", "function_args", "endorsers_id", "tx_status", "readkeys", "writekeys", "rangekeys", "transaction_type", "commit order", "case_id"]

home_dir = "/home/ubuntu/BlockProM/log_store/"
log_dir = ' '.join(sys.argv[1:])
full_path = home_dir + log_dir + "/csv"

#csv_path is the path to the output file, in which the extracted data is written in csv format
csv_path =full_path + "/clean_blockchainlog.csv"


file_dir=home_dir + log_dir

#writer = csv.writer(open('%s/metrics.csv' % full_path, 'w'))
#writer.writerow(["Metrics", "Variable_Name","Value"])

file = open(csv_path)
reader = csv.reader((x.replace('\0', '') for x in file), delimiter=',')
new_lines = list(reader)

n=0
TM=0

optcount = 0

#writer = csv.writer(open('%s/optrecs.csv' % full_path, 'a'))
#writer.writerow(["SlNo", "OptRec","Value"])


def is_phrase_in(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None

def __datetime(date_str):
    return datetime.strptime(date_str, '%a-%b-%d%T%H:%M:%S%Z')
    #2021-07-13T10:19:51.987Z

def rate_metrics():
    writer = csv.writer(open('%s/ratemetrics.csv' % full_path, 'w'))
    writer.writerow(["Metrics", "Variable_Name","Value"])

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

    writer = csv.writer(open('%s/failuremetrics.csv' % full_path, 'w'))
    writer.writerow(["Metrics", "Variable_Name","Value"])

    #TODO: Activity failure rate
    global n
    global TM
    global new_lines
    nf = 0
    nMRC = 0
    nEPF = 0
    nPRC = 0
    for i in range(1, len(new_lines)):
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
    writer.writerow(["Total Failure percent", "TFp",str((nf/n)*100)])
    writer.writerow(["MVCC read conflict", "MRC",str(nMRC)])
    writer.writerow(["MVCC read conflict rate", "MRCr",str(nMRC/TM)])
    writer.writerow(["MVCC read conflict percent", "MRCp",str((nMRC/n)*100)])
    writer.writerow(["Endorsement policy failure", "EPF",str(nEPF)])
    writer.writerow(["Endorsement policy failure rate", "EPFr",str(nEPF/TM)])
    writer.writerow(["Endorsement policy failure percent", "EPFp",str((nEPF/n)*100)])
    writer.writerow(["Phantom read conflict", "PRC",str(nPRC)])
    writer.writerow(["Phantom read conflict rate", "PRCr",str(nPRC/TM)])
    writer.writerow(["Phantom read conflict percent", "PRCp",str((nPRC/n)*100)])

    print()
    print(optcount, "Optimization recommendation: Implement all optimizations based on the number of transaction failures as listed below")
    print("Total number of transactions:", (len(new_lines) - 1))
    print("Total Failures:", nf)
    print("MVCC read conflict:", nMRC)
    print("Endorsement policy failure:", nEPF)
    print("Phantom read conflict:", nPRC)
    print()
    print("##########################################################################################")


def rate_distribution():
    #Total number of transactions in the log
    global n
    global new_lines
    writer = csv.writer(open('%s/rate_distribution.csv' % full_path, 'w'))
    writer.writerow(["Interval", "Tx Rate dist", "Failure Rate dist", "MVCC rd", "Phantom rf", "Endorsement rd", "ActivityFrequency"])
    #Time interval for distribution in seconds
    interval = 3 
    nt = 1
    ft = 0
    mt = 0
    pt = 0
    et = 0
    af=[]
    row=[]
    interval_count=0


    begin_time = arrow.get(new_lines[1][0]).datetime
    for i in range(2, len(new_lines)):
        nt = nt+1
        if new_lines[i][6] != "VALID":
            ft += 1
            af.append(new_lines[i][3])
            if new_lines[i][6] == "MVCC_READ_CONFLICT":
                mt += 1
            elif new_lines[i][6] == "ENDORSEMENT_POLICY_FAILURE":
                et += 1
            elif new_lines[i][6] == "PHANTOM_READ_CONFLICT":
                pt += 1
        #print(i)
        end_time = arrow.get(new_lines[i][0]).datetime
        duration = (end_time - begin_time).total_seconds()
        #print(duration)
        if duration >= interval:
            interval_count += 1
            trd = nt/duration
            frd = ft/duration
            mrd = mt/duration
            prd = pt/duration
            erd = et/duration
            af_counts = Counter(af)
            row.append([interval_count,trd,frd,mrd,prd,erd,af_counts])
            writer.writerows(row)
            nt=0
            ft=0
            mt = 0
            pt = 0
            et = 0
            af=[]
            row=[]
            duration=0
            if (i+1) < len(new_lines):
                begin_time = arrow.get(new_lines[i+1][0]).datetime


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
        endt = new_lines[i][5].split()
        for j in range(len(endt)):
            if i != 0 and endt[j] not in endorsers:
                endorsers.append(endt[j])

    edrows = [[None for _ in range(2)] for _ in range(len(endorsers))]

    for k in range(len(endorsers)):
        txcount = 0
        for i in range(len(new_lines)):
            if i != 0 and endorsers[k] in new_lines[i][5]:
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

    cpath = full_path + '/commitorder_cleanlog.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)



    writer = csv.writer(open('%s/datavalue_correlation.csv' % full_path, 'w'))
    writer.writerow(['Failed transaction','activity_name','Readset','WriteSet','RangeReadSet','Dependent transaction(valid)','activity_name','Readset','WriteSet','RangeReadSet','ReorderingPossibility', 'BlockNumberTx1', 'BlockNumberTx2', 'ProximityCorrelation'])
    
    dv=[]


    for i in range(1, len(cnew_lines)):
        if (cnew_lines[i][6] == "MVCC_READ_CONFLICT" or cnew_lines[i][6] == "PHANTOM_READ_CONFLICT"):
            for j in range(i-1, 0, -1):
                txstatus = cnew_lines[j][6]
                readseti = set(cnew_lines[i][7].split())
                writeseti = set(cnew_lines[i][8].split())
                rangeseti = set(cnew_lines[i][9].split())
                writesetj = set(cnew_lines[j][8].split())
                if ((txstatus == "VALID") and ((readseti != '') or (rangeseti != '')) and ((bool(readseti.intersection(writesetj)) == True) or (bool(rangeseti.intersection(writesetj)) == True))):
                    if (bool(writeseti.intersection(writesetj)) == False):
                        reorder = True
                    else:
                        reorder = False

                    if (cnew_lines[i][11] == cnew_lines[j][11]):
                        pcor = 0
                    else:
                        pcor = 1

                    dv.append([cnew_lines[i][1],cnew_lines[i][3],cnew_lines[i][7],cnew_lines[i][8],cnew_lines[i][9],cnew_lines[j][1],cnew_lines[j][3],cnew_lines[j][7],cnew_lines[j][8],cnew_lines[j][9],reorder,cnew_lines[i][11],cnew_lines[j][11],pcor])
                    break

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
    allendorsers=[]

    for i in range(1, len(cnew_lines)):
        if (int(cnew_lines[i][1]) > et1): 
            endorsers.append([cnew_lines[i][0], cnew_lines[i][1]])
        allendorsers.append([cnew_lines[i][0]])
        #print("All Endorsers:", cnew_lines[i][0],cnew_lines[i][1])

    if len(endorsers) < len(allendorsers):
        optcount += 1
        print()
        print(optcount, "Optimization recommendation: Redefine endorsement policy because endorser bottleneck was detected")
        print("More than", et1, "transactions out of", n, "transactions were endorsed by the set of endorsers:", endorsers)
        print("Try to distribute the endorsements equally among all the endorsers", allendorsers)
        print()
        print("##########################################################################################")
        writer = csv.writer(open('%s/optrecs.csv' % full_path, 'a'))
        writer.writerow([optcount, "Endorsement policy optimization", endorsers])

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

    rt_fail_tx_final = set(rt_fail_tx)

    #print(nRT)
    #print(nfRT)
    #print(rt_fail_tx)

    if nfRT > bat:
        optcount += 1
        print()
        print(optcount, "Optimization recommendation: Batch read transactions")
        print(nfRT," transactions out of",nRT," read transactions failed due to read conflicts. The failed transactions are:", rt_fail_tx_final)
        print()
        print("##########################################################################################")
        writer = csv.writer(open('%s/optrecs.csv' % full_path, 'a'))
        writer.writerow([optcount, "Read transaction batching", rt_fail_tx_final])

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
        writer = csv.writer(open('%s/optrecs.csv' % full_path, 'a'))
        writer.writerow([optcount, "Transaction reordering", reorderpairs_final])

def processprune():
    global n
    global new_lines
    global optcount
    processnames=[]
    pruneprocesslist=[]

    for i in range(1, (len(new_lines)-1)):
        processnames.append(new_lines[i][3])
    uniqueprocessnames=set(processnames)
    for pn in uniqueprocessnames:
        txtype=[]
        for i in range(1, (len(new_lines)-1)):
            if new_lines[i][3] == pn:
                if new_lines[i][10] != '':
                    txtype.append(new_lines[i][10])
        if len(set(txtype)) > 1:
            pruneprocesslist.append([pn, set(txtype)])

    if (len(pruneprocesslist) > 0):
        optcount += 1
        print()
        print(optcount, "Optimization recommendation: Possibility of process model pruning")
        print("Multiple transaction types detected for same process:")
        print(pruneprocesslist)
        print()
        print("##########################################################################################")
        writer = csv.writer(open('%s/optrecs.csv' % full_path, 'a'))
        writer.writerow([optcount, "Process model pruning possibility", pruneprocesslist])




def deltawrites():
    global n
    global new_lines
    global optcount
    cpath = full_path + '/datavalue_correlation.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)

    deltatx=[]
    for i in range(len(cnew_lines)-1):
        #if ((i != 0) and len(cnew_lines[i][8].split()) == 1):
        if (cnew_lines[i][8].isdigit()):
        
            if ((i != 0) and (len(cnew_lines[i][8].split()) == 1) and ((int(cnew_lines[i][8]) == int(cnew_lines[i+1][8])) or ((int(cnew_lines[i][8])+1) == int(cnew_lines[i+1][8])))):
            
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
        writer = csv.writer(open('%s/optrecs.csv' % full_path, 'a'))
        writer.writerow([optcount, "Delta-writes possibility", deltatx_final])

def blocksize_opt():
    global optcount
    bst1 = 1.6 #60% increase
    bst2 = 0.4 #60% decrease
    xpath = full_path + '/actual_blocksize.csv'
    xfile = open(xpath)
    xreader = csv.reader((x.replace('\0', '') for x in xfile), delimiter=',')
    xnew_lines = list(xreader)

    start_blknum = int(new_lines[1][11])
    total = 0
    count = 0

    for i in range((start_blknum+2), len(xnew_lines)):
        total += int(xnew_lines[i][1])
        count += 1

    actualbs = int(total/count)
    #print("Actual average block size", actualbs)

    ypath = full_path + '/config_blocksize.csv'
    yfile = open(ypath)
    yreader = csv.reader((x.replace('\0', '') for x in yfile), delimiter=',')
    ynew_lines = list(yreader)
    
    configbs = int(ynew_lines[0][1])
    #print("Configured block size", configbs)

    mpath = full_path + '/failuremetrics.csv'
    mfile = open(mpath)
    mreader = csv.reader((x.replace('\0', '') for x in mfile), delimiter=',')
    mnew_lines = list(mreader)
    totmvccfail = int(mnew_lines[4][2]) + int(mnew_lines[10][2])

    cpath = full_path + '/datavalue_correlation.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)
    intrafail = 0
    interfail = 0
    for i in range(1, len(cnew_lines)):
        if (cnew_lines[i][13] == '0'):
            intrafail += 1
        else:
            interfail += 1
    #print("intrafail", intrafail)
    #print("interfail", interfail)

    writer = csv.writer(open('%s/failuremetrics.csv' % full_path, 'a'))
    writer.writerow(["Intra-block failures", "intra",intrafail])
    writer.writerow(["Inter-block failures", "inter",interfail])

    ppath = full_path + '/rate_distribution.csv'
    pfile = open(ppath)
    preader = csv.reader((x.replace('\0', '') for x in pfile), delimiter=',')
    pnew_lines = list(preader)

    total = 0
    count = 0
    for i in range(1, len(pnew_lines)):
            total += float(pnew_lines[i][1])
            count += 1

    avgtxrate = round(total/count)

    #print("avgtxrate", avgtxrate)
    #print("actualbs", actualbs)
    if (avgtxrate > (actualbs*bst1)) or (avgtxrate < (actualbs*bst2)):
        optcount += 1
        print()
        print(optcount, "Optimization recommendation: Possibility of block size optimization detected")
        print("The average actual blocksize is", actualbs, "the configured block size is", configbs, "and the average transaction rate is", avgtxrate)
        print("Matching the block size to the average transaction rate might lead to better performance. ")
        print()
        print("##########################################################################################")
        writer = csv.writer(open('%s/optrecs.csv' % full_path, 'a'))
        writer.writerow([optcount, "Block size optimization", avgtxrate])

def splitbatch_chaincodes():
    global optcount
    global n

    cpath = full_path + '/key_significance.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)

    ht0 = n * 0.1
    ht1 = 3
    hotkey = cnew_lines[1][0]
    hotkeyfreq = float(cnew_lines[1][1])
    #print("hotkeyfreq",hotkeyfreq)
    #print("ht0",ht0)
    #len(set)
    if (hotkeyfreq > ht0):
        optcount += 1
        print()
        print(optcount, "Hot keys have been detected")
        print("The top", ht1, "hotkeys are shown below along with the type of smart contract optimization possible.")
        #print("Spliting chaincodes or batching within the chaincodes are possible optimizations to avoid conflicts:")
        print()
        writer = csv.writer(open('%s/optrecs.csv' % full_path, 'a'))
        writer.writerow([optcount, "Hot key detection", hotkey])
        for i in range(1, ht1+1):
            txnames=set(cnew_lines[i][2].split())
            print(i, "Key:", cnew_lines[i][0], "Frequency:", cnew_lines[i][1], "Transactions:", txnames)
            if len(txnames) == 1:
                print("Optimization recommendation: Redesign the data model related to the activity", txnames, "to avoid conflicts")
            else:
                print("Optimization recommendation: Spliting chaincodes or batching within the chaincodes are possible optimizations to avoid conflicts for the activities:",txnames)
    print()
    print("##########################################################################################")

def rate_control():
    global optcount
    cpath = full_path + '/rate_distribution.csv'
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)

    txratethreshold = 200
    failureratethreshold = (txratethreshold * 0.3)

    intervals=[]
    intervals.append(cnew_lines[0])

    for i in range(1, len(cnew_lines)):
        if (float(cnew_lines[i][1]) >= txratethreshold) and (float(cnew_lines[i][2]) >= failureratethreshold):
            intervals.append(cnew_lines[i])

    if (len(intervals) > 1):
        optcount += 1
        print()
        print(optcount, "Optimization recommendation: Possibility of rate control optimization detected")
        print("The following intervals have high failure rate and transaction rate. Consider rate control if such occurences are frequent")
        print("If the mined process model has a low fitness with the ideal process model, transaction rate control will help increase fitness")
        for i in range(len(intervals)):
            print(intervals[i])
        print()
        print("##########################################################################################")
        writer = csv.writer(open('%s/optrecs.csv' % full_path, 'a'))
        writer.writerow([optcount, "Transaction rate control", intervals])





#Metrics
rate_metrics()
failure_metrics()
originator_sig()
endorser_sig()
key_sig()
datavalue_correlation()
rate_distribution() #transactionrate, failurerate of each failure, activity failure rate, activity transaction rate

##blocksize()
##transactiontype_correlation()
##proximity_correlation()

#Optimization strategies
client_dist()
endorser_dist()
blocksize_opt()
##read_tx_batch()
rate_control()
tx_reordering()
deltawrites()
splitbatch_chaincodes()
processprune()

