#TODO: mkdir csv if it does not exist. If it exists then rm csv/*


#!/usr/bin/env python

import json
import os
import collections
import re
import csv
import sys

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

initfunc='InitLedger'

def is_phrase_in(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None

def activity_based_caseid(path):
    file = open(path)
    reader = csv.reader((x.replace('\0', '') for x in file), delimiter=',')
    new_lines = list(reader)
    for i in range(len(new_lines)):
        new_lines[i][11]=0

    activity_name=[]
    for i in range(len(new_lines)):
        if i != 0 and new_lines[i][3] != 'NULL' and new_lines[i][3] != 'deploy' and new_lines[i][3] != initfunc and new_lines[i][3] not in activity_name:
           activity_name.append(new_lines[i][3])

    for k in range(len(activity_name)):
        case_id=1
        for i in range(len(new_lines)):
            if i != 0 and new_lines[i][3]==activity_name[k]:
               new_lines[i][11]=case_id
               case_id+=1

    writer = csv.writer(open('%s/activity_based_caseid_blockchainlog.csv' % full_path, 'w'))
    writer.writerows(new_lines)


def key_based_caseid(path):
    unique_keys=[]
    file = open(path)
    reader = csv.reader((x.replace('\0', '') for x in file), delimiter=',')
    lines = list(reader)
    for i in range(len(lines)):
        lines[i][11]=0
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
        new_lines.append(["timestamp","tx_id","Mspid", "activity_name", "function_args", "endorsers_id", "tx_status", "readkeys", "writekeys", "rangekeys", "transaction_type", "case_id"])

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
                   new_lines[i][11]=case_id 
                   case_id+=1
        writer = csv.writer(open('%s/keybased/%s_blockchainlog.csv' % (full_path, key), 'w'))
        writer.writerows(new_lines)
    
    writer = csv.writer(open('%s/key_dependencies.csv' % full_path, 'w'))
    writer.writerows(key_dependencies)

 

key_based_caseid(csv_path)
activity_based_caseid(csv_path)

