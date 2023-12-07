# BlockOptR
An optimization recommender tool for blockchains (Hyperledger Fabric). This repository contains the research artifacts for this [SIGMOD 2023 paper](https://dl.acm.org/doi/abs/10.1145/3588704). It contains the BlockOptR source code (see description below), [smart contracts](chaincodes), [workload generation scripts](workloads), [event logs](event_logs), and [experimental results](results). The complete results for experiments with the synthetic workloads can be found [here](results/SyntheticWorkloads_CompleteResults.pdf).

# Quick Setup 
**This section is created for submission to the SIGMOD 2023 ARI and demonstrates that the artifacts are available and functional.** These scripts help users quickly set up a blockchain network, generate workloads, and test BlockOptR. It will set up a sample Hyperledger Fabric network and the Caliper benchmarking system on a single machine. A smart contract for a supply chain management scenario is installed on the blockchain, and a corresponding workload is executed. Then the BlockOptR tool is executed, which generates a list of optimization recommendations. Execute the following steps on a clean Ubuntu machine. These scripts were tested on Ubuntu 20.04 LTS and Ubuntu 22.04 LTS machines with 2vCPUS, 10GB memory and 10GB storage.

1. Clone this repository to the home directory (/home/ubuntu). Make sure the path is the same.
```shell
git clone https://github.com/jeetachacko/BlockOptR.git
```
2. Execute all the scripts from the BlockOptR folder
```shell
cd ~/BlockOptR
```
3. Install prerequisites
```shell
echo -ne '\n' | ./scripts/prerequisites1.sh
```
4. This script expects the entry of a password three times (any new password) - The script allows the use of Docker without sudo
```shell
./scripts/docker_setup.sh
```
5. Execute all the scripts from the BlockOptR folder
```shell
cd ~/BlockOptR
```
6. Install further prerequisites. Enter 'Y' when requested. Node dependency errors and warnings can be ignored.
```shell
./scripts/prerequisites2.sh
```
7. Setup the fabric network
```shell
./scripts/fabric_setup.sh simplesupplychain go
```
8. Setup the caliper benchmarking system and execute the workloads. Rerun this script if transactions remain unfinished. "MVCC_READ_CONFLICT", "PHANTOM_READ_CONFLICT" and "Peer endorsements do not match" errors are expected.
```shell
./scripts/caliper_setup.sh simplesupplychain go
```
9. Run BlockOptR - Optimization recommendations will be printed on the terminal
```shell
./scripts/blockoptr_run.sh
```
# Quick Setup - Further test cases
To change the workload, edit the "txNumber" (line 16) or "tps" (line 20) parameters in the file "workloads/simplesupplychain/config.yaml" for the label "common"
To change the smart contract, run steps 7, 8 and 9 with the new smart contract name and programming language name (shown below). The quick setup works with the following two smart contracts also. The workload for each of these smart contracts can also be changed as mentioned before.

Electronic Health Records:
./scripts/fabric_setup.sh electronic-health-record javascript
./scripts/caliper_setup.sh electronic-health-record javascript
./scripts/blockoptr_run.sh

E-Voting:
./scripts/fabric_setup.sh e-voting javascript
./scripts/caliper_setup.sh e-voting javascript
./scripts/blockoptr_run.sh

# BlockOptR on a Cluster
The following steps can set up Hyperledger Fabric and Caliper benchmarking system on an OpenStack cluster. BLockOptR is then set up with a more extensive log collection.
1. Setup [Hyperledger Lab](https://github.com/MSRG/HyperLedgerLab-2.0).  
2. Clone BlockOptR to a fabric client instance 
3. Replace the [connectionProfile](log_extraction/connectionprofile.yaml) with [hll_connectionProfile](log_extraction/hll_connectionprofile.yaml) to match the HyperledgerLab Fabric network
4. Execute ./scripts/full_script.sh <chaincode_name> <experiment_number>

What happens in the full script:
1. A new client is registered to Fabric and it extracts the full blockchain : [Blockchain Extraction Script](log_extraction/getBlockchainLogs.js)
2. Attributes are extracted/derived and a clean log is created in csv format : [Data Preprocessing Script](convert_to_csv/convert_blockchain_logs_to_csv.py)
3. CaseIDs and event log is generated : [CaseID/EventLog Generation Script](caseid_generation/caseid_generation.py) NOTE: Edit this script for new use-cases
4. Blockchain-specific metrics and optimization recommendations are derived : [Metrics/Recommendation Generation Script](metrics_evaluation/metrics_evaluation.py)

Additional details
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
