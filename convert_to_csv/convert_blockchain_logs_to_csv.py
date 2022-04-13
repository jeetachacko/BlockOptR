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

#fields contains the keys in json file which will be extracted. Extend this array if you want to extract other keys.
fields = ["timestamp","tx_id","Mspid", "activity_name", "function_args", "endorsers_id", "tx_status", "readkeys", "writekeys", "rangekeys", "transaction_type", "block number", "commit order", "case_id"]

home_dir = "/home/ubuntu/BlockOptR/log_store/"
log_dir = ' '.join(sys.argv[1:])
full_path = home_dir + log_dir + "/csv"

#csv_path is the path to the output file, in which the extracted data is written in csv format
csv_path =full_path + "/csvblockchain.csv"


file_dir=home_dir + log_dir


#initfunc='createElection'
initfunc='InitLedger'
#initfunc='CommitChaincodeDefinition'

def scan_files(path):
    
    getbs=0
    case_id=1
    blk_num=0
    commitorder=0

    bswriter = csv.writer(open('%s/actual_blocksize.csv' % full_path, 'w'))
    bswriter.writerow(["BlockNumber", "Number of transactions"])

    with open(csv_path,"w") as f:
       
        f.write("timestamp;tx_id;creatorid;activity_name;function_args;endorsers_id;tx_status;readkeys;writekeys;rangekeys;transaction_type;block number;commit order;case_id\n")
        f.close()
    dir_dict={}
    
    
    #all files in the directory are scanned, then the name, and extension of each file is extracted,
    #a dictionary is created in which keys are the index of each file, and the values are DirEntry of files
    #finaly in ordered_directory_dict all files are sorted based on their indecies
    for file_path in os.scandir(path):
        
        if file_path.is_file():
            base_name= os.path.basename(file_path)
            name, extension = os.path.splitext(base_name)

            if(extension ==".json"):
                dir_dict[int(name)]= file_path
    ordered_directory_dict=collections.OrderedDict(sorted(dir_dict.items()))
        
   
    #looping through all json files 
    for _ , file_path in ordered_directory_dict.items():
        
 
        file_values=[]
    
        #reading one file
        with open(file_path) as json_file:
           
            try:
                json_data = json.load(json_file)
            except Exception:
                pass

            #TIMESTAMP
            field_values=[]
            try:
                res = json_data['data']['data']
                res_len = len(json_data['data']['data'])
                for x in range(res_len):
                    ires = res[x]['payload']['header']['channel_header']['timestamp']
                    field_values.append(ires)
            except Exception:
                field_values.append("NULL")
                pass

            file_values.append(field_values)

            #TX_ID
            field_values=[]
            try:
                res = json_data['data']['data']
                res_len = len(json_data['data']['data'])
                for x in range(res_len):
                    ires = res[x]['payload']['header']['channel_header']['tx_id']
                    field_values.append(ires)
            except Exception:
                field_values.append("NULL")
                pass

            file_values.append(field_values)

            #CREATOR_ID
            field_values=[]
            try:
                res = json_data['data']['data']
                res_len = len(json_data['data']['data'])
                for x in range(res_len):
                    ires = res[x]['payload']['header']['signature_header']['creator']['Mspid']
                    field_values.append(ires)
            except Exception:
                field_values.append("NULL")
                pass

            file_values.append(field_values)



            #FUNCTION_NAME     
            field_values=[]
            try:
                res = json_data['data']['data']
                res_len = len(json_data['data']['data'])
                for x in range(res_len):
                    ires = res[x]['payload']['data']['actions'][0]['payload']['chaincode_proposal_payload']['input']['chaincode_spec']['input']['args'][0]['data']
                    restr = bytes(ires).decode("utf8")
                    field_values.append(restr)
            except Exception:
                field_values.append("NULL")
                pass

            file_values.append(field_values)

            #FUNCTION_ARGS
            field_values=[]
            try:
                res = json_data['data']['data']
                res_len = len(json_data['data']['data'])
                for x in range(res_len):
                    arg_new = res[x]['payload']['data']['actions'][0]['payload']['chaincode_proposal_payload']['input']['chaincode_spec']['input']['args'][1]['data']
                    restr = bytes(arg_new).decode("utf8")
                    field_values.append(restr)
            except Exception:
                field_values.append("NULL")
                pass

            file_values.append(field_values)

            #ENDORSERS
            field_values=[]
            try:
                res = json_data['data']['data']
                res_len = len(json_data['data']['data'])
                for x in range(res_len):
                    restr = ''
                    endorsements = res[x]['payload']['data']['actions'][0]['payload']['action']['endorsements']
                    endl = len(res[x]['payload']['data']['actions'][0]['payload']['action']['endorsements'])
                    for y in range(endl):
                        eachend = endorsements[y]['endorser']['Mspid']
                        restr += eachend
                        restr += ' ' 
                    field_values.append(restr)
            except Exception:
                field_values.append("NULL")
                pass

            file_values.append(field_values)

            #TX_STATUS
            tx_failures = ["VALID", "NIL_ENVELOPE", "BAD_PAYLOAD", "BAD_COMMON_HEADER", "BAD_CREATOR_SIGNATURE", "INVALID_ENDORSER_TRANSACTION", "INVALID_CONFIG_TRANSACTION", "UNSUPPORTED_TX_PAYLOAD", "BAD_PROPOSAL_TXID", "DUPLICATE_TXID", "ENDORSEMENT_POLICY_FAILURE", "MVCC_READ_CONFLICT", "PHANTOM_READ_CONFLICT", "UNKNOWN_TX_TYPE", "TARGET_CHAIN_NOT_FOUND", "MARSHAL_TX_ERROR", "NIL_TXACTION", "EXPIRED_CHAINCODE", "CHAINCODE_VERSION_CONFLICT", "BAD_HEADER_EXTENSION", "BAD_CHANNEL_HEADER", "BAD_RESPONSE_PAYLOAD", "BAD_RWSET", "ILLEGAL_WRITESET", "INVALID_WRITESET", "INVALID_CHAINCODE", "NOT_VALIDATED", "INVALID_OTHER_REASON"]

            field_values=[]
            try:
                res = json_data['metadata']['metadata'][2]
                res_len = len(res)
                for x in range(res_len):
                    tx_status = tx_failures[res[x]]
                    if res[x] == 254:
                       tx_status = tx_failures[26]
                    elif res[x] == 255:
                       tx_status = tx_failures[27]
                    field_values.append(tx_status)
            except Exception:
                field_values.append("NULL")
                pass

            file_values.append(field_values)

            #READ_KEYS
            field_values=[]
            try:
                res = json_data['data']['data']
                res_len = len(json_data['data']['data'])
                for x in range(res_len):
                    readkeys=''
                    #numreads = len(res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][0]['rwset']['reads'])
                    numreads = len(res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][1]['rwset']['reads'])
                    for y in range(numreads):
                        #key = res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][0]['rwset']['reads'][y]['key']   
                        key = res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][1]['rwset']['reads'][y]['key']   
                        readkeys = readkeys + ' ' + key
                    field_values.append(readkeys)
            except Exception:
                field_values.append("NULL")
                pass

            file_values.append(field_values)


            #WRITE_KEYS
            field_values=[]
            try:
                res = json_data['data']['data']
                res_len = len(json_data['data']['data'])
                for x in range(res_len):
                    writekeys=''
                    #numwrites = len(res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][0]['rwset']['writes'])
                    numwrites = len(res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][1]['rwset']['writes'])

                    for y in range(numwrites):
                        #key = res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][0]['rwset']['writes'][y]['key']
                        key = res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][1]['rwset']['writes'][y]['key']
                        writekeys = writekeys + ' ' + key
                    field_values.append(writekeys)
            except Exception:
                field_values.append("NULL")
                pass

            file_values.append(field_values)


            #RANGE_KEYS
            field_values=[]
            try:
                res = json_data['data']['data']
                res_len = len(json_data['data']['data'])
                for x in range(res_len):
                    try:
                        rangekeys=''
                        range_len = len(res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][1]['rwset']['range_queries_info'])
                        for q in range(range_len):
                            #numrange = len(res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][0]['rwset']['range_queries_info'][q]['raw_reads']['kv_reads'])
                            numrange = len(res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][1]['rwset']['range_queries_info'][q]['raw_reads']['kv_reads'])
                            for y in range(numrange):
                                #key = res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][0]['rwset']['range_queries_info'][q]['raw_reads']['kv_reads'][y]['key']
                                key = res[x]['payload']['data']['actions'][0]['payload']['action']['proposal_response_payload']['extension']['results']['ns_rwset'][1]['rwset']['range_queries_info'][q]['raw_reads']['kv_reads'][y]['key']
                                rangekeys = rangekeys + ' ' + key
                        field_values.append(rangekeys)
                    except Exception:
                        field_values.append("NULL")
                        pass
            except Exception:
                #print(Exception)
                field_values.append("NULL")
                pass

            file_values.append(field_values)

            #BLOCK SIZE
            if(getbs==0):
                try:
                    res = json_data['data']['data']
                    blocksize = res[0]['payload']['data']['config']['channel_group']['groups']['Orderer']['values']['BatchSize']['value']['max_message_count']
                    maxbytes = res[0]['payload']['data']['config']['channel_group']['groups']['Orderer']['values']['BatchSize']['value']['absolute_max_bytes']
                    preferredmaxbytes = res[0]['payload']['data']['config']['channel_group']['groups']['Orderer']['values']['BatchSize']['value']['preferred_max_bytes']
                    blocktimeout = res[0]['payload']['data']['config']['channel_group']['groups']['Orderer']['values']['BatchTimeout']['value']['timeout']
                    #print(blocksize)
                    getbs=1
                    writer = csv.writer(open('%s/config_blocksize.csv' % full_path, 'w'))
                    writer.writerow(["Blocksize", blocksize])
                    writer.writerow(["absolute_max_bytes", maxbytes])
                    writer.writerow(["preferred_max_bytes", preferredmaxbytes])
                    writer.writerow(["timeout", blocktimeout])


                except Exception:
                    print(Exception)




            #TransactionType
            field_values=[]
            field_values.append("")
            file_values.append(field_values)


            #BlockNumber
            field_values=[]
            try:
                res = json_data['data']['data']
                res_len = len(json_data['data']['data'])
                bswriter.writerow([blk_num, res_len])
                for x in range(res_len):
                    field_values.append(blk_num)
                blk_num += 1
            except Exception:
                field_values.append(blk_num)
                blk_num += 1
                pass

            file_values.append(field_values)

            #Commit order
            field_values=[]
            try:
                res = json_data['data']['data']
                res_len = len(json_data['data']['data'])
                for x in range(res_len):
                    field_values.append(commitorder)
                    commitorder += 1
            except Exception:
                field_values.append(commitorder)
                commitorder += 1
                pass

            file_values.append(field_values)




            json_file.close()

        case_id=csv_write(fields,file_values,csv_path,case_id)
    new_csv_path=get_transaction_status(csv_path)
    organizelog=organize_log(new_csv_path)



def csv_write(fields, data,path,case_id):
    
    
    count=0
    with open(path,"a") as f:
        
        i = 0

        for i in range(len(data[0])):

            for j in range(len(data)):
                                    
                if (i < len(data[j])):
                    f.write("\"%s\"" % data[j][i])
                    
                    #if(data[j][i]=="viewEHR"):
                    #    case_id+=1
                    #    count=1
                else:
                    f.write("\"\"")
                if(j < len(data)-1):
                    f.write(";")
            f.write(";")
            f.write(str(case_id))
            f.write("\n")
        
        #if(count == 0):
        #    case_id+=1
        
        f.close()
        return case_id
    

def get_transaction_status(path):
    rk = 1
    wk = 1
    rrk = 1
    file = open(path)
    reader = csv.reader((x.replace('\0', '') for x in file), delimiter=';')
    new_lines = list(reader)
    for i in range(len(new_lines)):
        new_lines[i][13]=0

    for i in range(len(new_lines)):
        if i != 0 and new_lines[i][3] != 'NULL' and new_lines[i][3] != 'deploy' and new_lines[i][3] != initfunc:
            if new_lines[i][7] == 'NULL' or new_lines[i][7] == '' or new_lines[i][7] is None or new_lines[i][7] == "":
                rk=0
            if new_lines[i][8] == 'NULL' or new_lines[i][8] == '' or new_lines[i][8] is None or new_lines[i][8] == "":
                wk=0
            if new_lines[i][9] == 'NULL' or new_lines[i][9] == '' or new_lines[i][9] is None or new_lines[i][9] == "":
                rrk=0
            #print(rk, wk, rrk)
            if (rk == 0 and rrk == 0 and wk == 1):
                new_lines[i][10] = "WT"
            elif (rk == 1 and rrk == 0 and wk == 0):
                new_lines[i][10] = "RT"
            elif ((rk == 1 or rrk == 1) and wk == 1):
                new_lines[i][10] = "UT"
            elif (rk == 0 and rrk ==1 and wk == 0):
                new_lines[i][10] = "RRT"
            elif ((rk == 1 or rrk == 1) and wk == 0):
                new_lines[i][10] = "RT*"
            rk = 1
            rrk = 1
            wk = 1


    writer = csv.writer(open('%s/main_blockchainlog.csv' % full_path, 'w'))
    writer.writerows(new_lines)
    new_csv_path = full_path + '/main_blockchainlog.csv'
    return new_csv_path

def organize_log(path):
    file = open(path)
    reader = csv.reader((x.replace('\0', '') for x in file), delimiter=',')
    new_lines = list(reader)
    setline = 0
    length = 0
    for i in range(len(new_lines)):
        if new_lines[i][3] == initfunc:
            setline = 1
        if setline == 1 and new_lines[i][3] != initfunc:
            length = i
            break
    if length > 0:
        for i in range(1, length):
            del new_lines[1]

    new_lines_final = [v for v in new_lines if v[3] != initfunc]
    new_lines_sort = sorted(new_lines_final,key=lambda l:l[0])
    writer = csv.writer(open('%s/clean_blockchainlog.csv' % full_path, 'w'))
    writer.writerow(new_lines_sort[len(new_lines_sort)-1])
    for i in range(len(new_lines_sort)-1):
        writer.writerow(new_lines_sort[i])

    new_lines_csort = sorted(new_lines_final,key=lambda l:l[12])
    cwriter = csv.writer(open('%s/commitorder_cleanlog.csv' % full_path, 'w'))
    cwriter.writerow(new_lines_csort[len(new_lines_csort)-1])
    for i in range(len(new_lines_csort)-1):
        cwriter.writerow(new_lines_csort[i])


def is_phrase_in(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None

def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


scan_files(file_dir)
