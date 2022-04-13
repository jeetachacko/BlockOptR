# BlockOptR
An optimization recommender tool for blockchains (Hyperledger Fabric).

# Steps to execute BlockOptR
1. Setup Hyperledger Fabric [Fabric Setup Docs](https://hyperledger-fabric.readthedocs.io/en/release-2.2/getting_started.html).  
2. Clone BlockOptR to a fabric client instance 
3. Edit the[connectionProfile](log_extraction/connectionprofile.yaml) to match the Fabric network
4. Execute ./scripts/full_script.sh <chaincode_name> <experiment_number>

# What happens in the full script:
1. A new client is registered to Fabric and it extracts the full blockchain [Blockchain Extraction Script](log_extraction/getBlockchainLogs.js)
2. Attributes are extracted/derived and a clean log is created in csv format [Data Preprocessing Script](convert_to_csv/convert_blockchain_logs_to_csv.py)
3. CaseIDs and event log is generated [CaseID/EventLog Generation Script](caseid_generation/caseid_generation.py) NOTE: Edit this script for new use-cases
4. Blockchain-specific metrics and optimization recommendations are derived [Metrics/Recommendation Generation Script](metrics_evaluation/metrics_evaluation.py)
