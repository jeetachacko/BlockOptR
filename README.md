# BlockOptR
An optimization recommender tool for blockchains (Hyperledger Fabric). This repository contains the research artifacts for this [SIGMOD paper](https://dl.acm.org/doi/abs/10.1145/3588704). It contains the BlockOptR source code (see description below), [smart contracts](chaincodes), [workload generation scripts](workloads), [event logs](event_logs), and [experimental results](results). The complete results for experiments with the synthetic workloads can be found [here](results/SyntheticWorkloads_CompleteResults.pdf).

# Quick Setup 
Execute the following steps on a clean Ubuntu machine. The following scripts will set up a sample Hyperledger Fabric network and the Caliper benchmarking system on a single Ubuntu machine. A smart contract for a supply chain management scenario is installed on the blockchain, and a corresponding workload is executed. Then the BlockOptR tool is executed, which generates a list of optimization recommendations.

Clone this repository to the home directory
```shell
git clone git@github.com:jeetachacko/BlockOptR.git
```
Execute all the scripts from the BlockOptR folder
```shell
cd ~/BlockOptR
```
Install prerequisites
```shell
echo -ne '\n' | ./scripts/prerequisites1.sh
```
This script expects the entry of a password three times (any new password) - The script allows the use of without sudo
```shell
./scripts/docker_setup.sh
```
Execute all the scripts from the BlockOptR folder
```shell
cd ~/BlockOptR
```
Install further prerequisites
```shell
./scripts/prerequisites2.sh
```
Setup the fabric network
```shell
./scripts/fabric_setup.sh simplesupplychain go
```
Setup the caliper benchmarking system and execute the workloads
```shell
./scripts/caliper_setup.sh simplesupplychain go
```
Run BlockOptR - Optimization recommendations will be printed on the terminal
```shell
./scripts/blockoptr_run.sh
```



# Steps to execute BlockOptR on a CLuster
1. [Setup Hyperledger Fabric](https://hyperledger-fabric.readthedocs.io/en/release-2.2/getting_started.html).  
2. Clone BlockOptR to a fabric client instance 
3. Edit the [connectionProfile](log_extraction/connectionprofile.yaml) to match the Fabric network
4. Execute ./scripts/full_script.sh <chaincode_name> <experiment_number>

# What happens in the full script:
1. A new client is registered to Fabric and it extracts the full blockchain : [Blockchain Extraction Script](log_extraction/getBlockchainLogs.js)
2. Attributes are extracted/derived and a clean log is created in csv format : [Data Preprocessing Script](convert_to_csv/convert_blockchain_logs_to_csv.py)
3. CaseIDs and event log is generated : [CaseID/EventLog Generation Script](caseid_generation/caseid_generation.py) NOTE: Edit this script for new use-cases
4. Blockchain-specific metrics and optimization recommendations are derived : [Metrics/Recommendation Generation Script](metrics_evaluation/metrics_evaluation.py)

# Additional details
1. [Blockchain Extraction Script](log_extraction/getBlockchainLogs.js)  
    + **Input:** [connectionProfile](log_extraction/connectionprofile.yaml)
    + **Output:** log_extraction/data/\<multiple json files\>

2. [Data Preprocessing Script](convert_to_csv/convert_blockchain_logs_to_csv.py)              
    + **Input:** log_extraction/data/\<multiple json files\>              
    + **Output:** log_store/\<autogen directory name\>/csv/\<multiple csv files\>  
      - main_blockchainlog.csv
      - clean_blockchainlog.csv
      - commitorder_cleanlog.csv
      - csvblockchain.csv
      - actual_blocksize.csv
      - config_blocksize.csv

3. [CaseID/EventLog Generation Script](caseid_generation/caseid_generation.py)              
    + **Input:** log_store/\<autogen directory name\>/csv/clean_blockchainlog.csv              
    + **Output:** log_store/\<autogen directory name\>/csv/new_activity_basedcaseid_blockchainlog.csv  

4. [Metrics/Recommendation Generation Script](metrics_evaluation/metrics_evaluation.py)              
    + **Input:** log_store/\<autogen directory name\>/csv/\<multiple csv files\>
      - clean_blockchainlog.csv
      - commitorder_cleanlog.csv
      - actual_blocksize.csv
      - config_blocksize.csv              
    + **Output:** log_store/\<autogen directory name\>/csv/\<multiple csv files\>
      - originator_significance.csv
      - endorser_significance.csv
      - datavalue_correlation.csv
      - failuremetrics.csv
      - rate_distribution.csv
      - key_significance.csv

**NOTE 1: The [full_script](scripts/full_script.sh) assumes the deployment of Fabric using the HyperledgerLab2 testbed. Modify the script accordingly to match other deployments of Fabric**  


[//]: # (HyperledgerLab2 https://github.com/MSRG/HyperLedgerLab-2.0)
