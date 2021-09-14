# BlockProM
An optimization strategy detection tool for blockchains (Hyperledger Fabric) using process mining.
# Steps to execute BlockProM
1. Setup Hyperledger Fabric   
2. Clone BlockProM to a fabric client instance 
3. Edit the connectionProfile to match the Fabric network (log_extraction/connectionprofile.yaml) 
4. Execute scripts/full_script.sh 

#What happens:
1. A new client is registered to Fabric and it extracts the full blockchain (log_extraction/getBlockchainLogs.js)
2. Process attributes are extracted and an event log is created in csv format (convert_to_csv/convert_blockchain_logs_to_csv.py)
3. Two types of caseIDs are generated (caseid_generation/caseid_generation.py : Edit this file for new use-cases)
4. Blockchain-specific metrics and optimization strategies are derived (metrics_evaluation/metrics_evaluation.py)
