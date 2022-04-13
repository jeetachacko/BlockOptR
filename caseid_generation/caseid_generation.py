#TODO: mkdir csv if it does not exist. If it exists then rm csv/*


#!/usr/bin/env python

import json
import os
import collections
import re
import csv
import sys
import numpy as np

#the extract function is used from: 
#https://hackersandslackers.com/extract-data-from-complex-json-python/

#fields contains the keys in json file which will be extracted
fields = ["timestamp","tx_id","Mspid", "activity_name", "function_args", "endorsers_id", "tx_status", "readkeys", "writekeys", "rangekeys", "transaction_type", "block number", "commit order", "case_id"]

home_dir = "/home/ubuntu/BlockOptR/log_store/"
log_dir = ' '.join(sys.argv[1:])
#log_dir = str(sys.argv[1])
#usecase = str(sys.argv[2])
full_path = home_dir + log_dir + "/csv"

#csv_path is the path to the output file, in which the extracted data is written in csv format
csv_path =full_path + "/clean_blockchainlog.csv"


file_dir=home_dir + log_dir

#Replace this with the name of the init function of the specific use case
initfunc='InitLedger'

def is_phrase_in(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None

#Unused function
def activity_based_caseid(path):
    file = open(path)
    reader = csv.reader((x.replace('\0', '') for x in file), delimiter=',')
    new_lines = list(reader)
    for i in range(len(new_lines)):
        new_lines[i][13]=0

    activity_name=[]
    for i in range(len(new_lines)):
        if i != 0 and new_lines[i][3] != 'NULL' and new_lines[i][3] != 'deploy' and new_lines[i][3] != initfunc and new_lines[i][3] not in activity_name:
           activity_name.append(new_lines[i][3])

    for k in range(len(activity_name)):
        case_id=1
        for i in range(len(new_lines)):
            if i != 0 and new_lines[i][3]==activity_name[k]:
               new_lines[i][13]=case_id
               case_id+=1

    writer = csv.writer(open('%s/activity_based_caseid_blockchainlog.csv' % full_path, 'w'))
    writer.writerows(new_lines)

#Unused function
def key_based_caseid(path):
    unique_keys=[]
    file = open(path)
    reader = csv.reader((x.replace('\0', '') for x in file), delimiter=',')
    lines = list(reader)
    for i in range(len(lines)):
        lines[i][13]=0
    for i in range(len(lines)):
        readkey = []
        writekey = []
        rangekey = []
        if i != 0 and lines[i][3] != 'NULL' and lines[i][3] != 'deploy' and lines[i][3] != initfunc:
           readkey += (lines[i][7].strip()).split()
           for k in readkey:
             if k not in unique_keys and k != 'NULL' and k != '':
                unique_keys.append(k)
           writekey += (lines[i][8].strip()).split()
           for k in writekey:
             if k not in unique_keys and k != 'NULL' and k != '':
                unique_keys.append(k)
           rangekey += (lines[i][9].strip()).split()
           for k in rangekey:
             if k not in unique_keys and k != 'NULL' and k != '':
                unique_keys.append(k)

    key_dependencies=[]
    key_dependencies.append(['keys','number_of_dependencies'])
    #print(unique_keys)
    for key in unique_keys:
        numdependencies=0
        new_lines=[]
        new_lines.append(["timestamp","tx_id","Mspid", "activity_name", "function_args", "endorsers_id", "tx_status", "readkeys", "writekeys", "rangekeys", "transaction_type", "block number", "commit order", "case_id"])

        for i in range(len(lines)):
            if i != 0 and lines[i][3] != 'NULL' and lines[i][3] != 'deploy' and lines[i][3] != initfunc:
               if (key != '') and (is_phrase_in(key, lines[i][7].strip()) or is_phrase_in(key, lines[i][8].strip()) or is_phrase_in(key, lines[i][9].strip())):
                   new_lines.append(lines[i])
                   numdependencies+=1
        key_dependencies.append([key,numdependencies]) 

        activity_name=[]
        for i in range(len(new_lines)):
            if new_lines[i][3] not in activity_name:
               activity_name.append(new_lines[i][3])
        for k in range(len(activity_name)):
            case_id=1
            for i in range(len(new_lines)):
                if new_lines[i][3]==activity_name[k]:
                   new_lines[i][13]=case_id 
                   case_id+=1
        writer = csv.writer(open('%s/keybased/%s_blockchainlog.csv' % (full_path, key), 'w'))
        writer.writerows(new_lines)
    
    writer = csv.writer(open('%s/key_dependencies.csv' % full_path, 'w'))
    writer.writerows(key_dependencies)

 #Unused function
def new_key_based_caseid(path):
    unique_keys=[]
    file = open(path)
    reader = csv.reader((x.replace('\0', '') for x in file), delimiter=',')
    lines = list(reader)
    for i in range(len(lines)):
        lines[i][13]=0
    for i in range(len(lines)):
        readkey = []
        writekey = []
        rangekey = []
        if i != 0 and lines[i][3] != 'NULL' and lines[i][3] != 'deploy' and lines[i][3] != initfunc:
           readkey += (lines[i][7].strip()).split()
           for k in readkey:
             if k not in unique_keys and k != 'NULL' and k != '':
                unique_keys.append(k)
           writekey += (lines[i][8].strip()).split()
           for k in writekey:
             if k not in unique_keys and k != 'NULL' and k != '':
                unique_keys.append(k)
           rangekey += (lines[i][9].strip()).split()
           for k in rangekey:
             if k not in unique_keys and k != 'NULL' and k != '':
                unique_keys.append(k)

    key_dependencies=[]
    key_dependencies.append(['keys','number_of_dependencies'])
    #print(unique_keys)
    new_lines=[]
    new_lines.append(["timestamp","tx_id","Mspid", "activity_name", "function_args", "endorsers_id", "tx_status", "readkeys", "writekeys", "rangekeys", "transaction_type", "block number", "commit order", "case_id"])
    for key in unique_keys:
        numdependencies=0

        for i in range(len(lines)):
            if i != 0 and lines[i][3] != 'NULL' and lines[i][3] != 'deploy' and lines[i][3] != initfunc:
               if (key != '') and (is_phrase_in(key, lines[i][7].strip()) or is_phrase_in(key, lines[i][8].strip()) or is_phrase_in(key, lines[i][9].strip())):
                   lines[i][13]=key
                   new_lines.append(lines[i].copy())
                   numdependencies+=1
        key_dependencies.append([key,numdependencies])

        #activity_name=[]
        #for i in range(len(new_lines)):
        #    if new_lines[i][3] not in activity_name:
        #       activity_name.append(new_lines[i][3])
        #for k in range(len(activity_name)):
        #    case_id=1
        #    for i in range(len(new_lines)):
        #        if new_lines[i][3]==activity_name[k]:
        #           new_lines[i][13]=case_id
        #           case_id+=1

        
    writer = csv.writer(open('%s/keybasedcaseid_blockchainlog.csv' % (full_path), 'w'))
    writer.writerows(new_lines)

    writer = csv.writer(open('%s/key_dependencies.csv' % full_path, 'w'))
    writer.writerows(key_dependencies)

#The main case id and event log generation function
def new_activity_based_caseid(path):

    #Edit this part of the code based on the use case
    #################################################
    #0=SCM;1=DRM;2=DV;3=EHR; 4=LAP; 5=SSCM
    usecase=5

    unique_keys=[]
    file = open(path)
    reader = csv.reader((x.replace('\0', '') for x in file), delimiter=',')
    headers = next(reader)
    headers.append("CommonKey")
    lines = list(reader)
    for row in lines:
        row.append('0')
    print(headers)
    for i in range(len(lines)):
        lines[i][13]=0

    next_lines=[]
    next_lines.append(headers.copy())

        #################################################
        #Duplicating activities
        #Edit this part of the code based on the use case
        #################################################

        #0=SCM;1=DRM;2=DV;3=EHR; 5=SSCM


    if usecase==1:
        for i in range(len(lines)):
            if lines[i][3] == 'calcRevenue':
                readkeys=(lines[i][7].strip()).split()
                if len(readkeys) > 0:
                    for j in range(len(readkeys)):
                        next_lines.append(lines[i].copy())
                        next_lines[-1][7]=readkeys[j]
                else:
                    next_lines.append(lines[i].copy())

            else:
                next_lines.append(lines[i].copy())
    else:
        for i in range(len(lines)):
            rangekeys=(lines[i][9].strip()).split()
            if len(rangekeys) > 0:
                for j in range(len(rangekeys)):
                    next_lines.append(lines[i].copy())
                    next_lines[-1][9]=rangekeys[j]
            else:
                next_lines.append(lines[i].copy())

    #################################################

    writer = csv.writer(open('%s/new_duplicatedactivities_blockchainlog.csv' % (full_path), 'w'))
    writer.writerows(next_lines)

    lines = []
    new_path =full_path + "/new_duplicatedactivities_blockchainlog.csv"
    file = open(new_path)
    reader = csv.reader((x.replace('\0', '') for x in file), delimiter=',')
    lines = list(reader)
    for i in range(1,len(lines)):
        lines[i][13]=0

        #################################################
        #Deriving the common key for all activities
        #Edit this part of the code based on the use case
        #################################################

        #0=SCM;1=DRM;2=DV;3=EHR; 5=SSCM

        #################################################
        #5. SSCM
        if usecase==5:
            if (lines[i][3] == 'QueryProducts'):
                rangekey=lines[i][9]
                lines[i][14] = rangekey
            else:
                funcargs=(lines[i][4].strip()).split()
                lines[i][14] = funcargs[0]
        #################################################
        #0. SCM
        #################################################
    
        if usecase==0:
            if (lines[i][3] == 'pushASN') or (lines[i][3] == 'queryLogisticUnit') or (lines[i][3] == 'ship') or (lines[i][3] == 'unload') :
                funcargs=(lines[i][4].strip()).split()
                if len(funcargs) > 0:
                    lines[i][14] = funcargs[0]
            elif (lines[i][3] == 'queryASN'):
                #rangekeys=(lines[i][9].strip()).split()
                #newrangekeys=[]
                #for x in range(len(rangekeys)):
                #    temp=rangekeys[x]
                #    newrangekeys.append(temp[4:])
                rangekey=lines[i][9]
                lines[i][14] = rangekey[4:]
                #lines[i][14] = newrangekeys
        #################################################

        #################################################
        #1. DRM
        if usecase==1:

            mapkeys={}
            for k in range(1,len(lines)):
                if (lines[k][3] == 'play'):
                    writekeys=(lines[k][8].strip()).split()
                    funcargs=(lines[k][4].strip()).split()
                    if len(writekeys) > 0:
                        mapkeys[writekeys[0]] = funcargs[0]

            if (lines[i][3] == 'play') or (lines[i][3] == 'queryRightHolders') or (lines[i][3] == 'viewMetaData'):
                funcargs=(lines[i][4].strip()).split()
                lines[i][14] = funcargs[0]
            elif (lines[i][3] == 'calcRevenue'):
                readkey=lines[i][7]
                if readkey:
                    mapid=readkey
                    if mapid in mapkeys:
                        lines[i][14] = mapkeys[mapid]
            elif (lines[i][3] == 'create'):
                writekeys=(lines[i][8].strip()).split()
                if len(writekeys) > 1:
                    mapid=writekeys[1]
                    if mapid in mapkeys:
                        lines[i][14] = mapkeys[mapid]
        #################################################

        #################################################
        #2. DV
        if usecase==2:
            readkeys=(lines[i][7].strip()).split()
            if len(readkeys) > 0:
                lines[i][14] = readkeys[0]
        #################################################

        #################################################
        #3. EHR
        if usecase==3:
            mapkeys={}
            for k in range(1,len(lines)):
                if (lines[k][3] == 'grantEHRAccess'):
                    readkeys=(lines[k][7].strip()).split()
                    funcargs=(lines[k][4].strip()).split()
                    if len(readkeys) > 1:
                        mapkeys[readkeys[1]] = funcargs[0]

            if (lines[i][3] == 'viewEHR'):
                funcargs=(lines[i][4].strip()).split()
                mapid=funcargs[0]
                if mapid in mapkeys:
                    lines[i][14] = mapkeys[mapid]
            else:
                funcargs=(lines[i][4].strip()).split()
                lines[i][14] = funcargs[0]
        #################################################
        #################################################
        #4. LAP
        if usecase==4:
            writekeys=(lines[i][8].strip()).split()
            if len(writekeys) > 0:
                lines[i][14] = writekeys[0]
        #################################################

    new_lines=[]
    new_lines.append(headers.copy())
    #new_lines.append(lines[0].copy())
    caseid=1
    for i in range(1, len(lines)):
        activity_name=[]
        #removes activities that do not have a common key
        if (lines[i][14]=='0') or (lines[i][14]==0) or (lines[i][14] is None):
            lines[i][14]=0
            #uncomment below line if you want caseid 0 for activities with no common key
            #new_lines.append(lines[i].copy())
            continue
        if lines[i][13] == 0:
            lines[i][13]=caseid
            activity_name.append(lines[i][3])
            for j in range((i+1), len(lines)):
                if (lines[j][3] not in activity_name) and (lines[j][13] == 0):
                    #if (lines[j][3] == 'queryASN'):
                    #    if lines[i][14] in lines[j][14]:
                    #        lines[j][13]=caseid
                    #        activity_name.append(lines[j][3])
                    if lines[i][14] == lines[j][14]:
                        lines[j][13]=caseid
                        activity_name.append(lines[j][3])
            caseid+=1
        new_lines.append(lines[i].copy())


    writer = csv.writer(open('%s/new_activity_basedcaseid_blockchainlog.csv' % (full_path), 'w'))
    writer.writerows(new_lines)



#new_key_based_caseid(csv_path)
new_activity_based_caseid(csv_path)
#key_based_caseid(csv_path)
#activity_based_caseid(csv_path)

