#!/usr/bin/env bash
set +ex

chaincode=fastfabric
expnum=1

cd /home/ubuntu/BlockProM

rm log_extraction/data/*
rm -rf log_store/*

cd /home/ubuntu/go/src/github.com/hyperledger/fabric/fastfabric/scripts/client
source /home/ubuntu/go/src/github.com/hyperledger/fabric/fastfabric/scripts/base_parameters.sh
source /home/ubuntu/go/src/github.com/hyperledger/fabric/fastfabric/scripts/custom_parameters.sh
node getBlockchainLogs.js
mv /home/ubuntu/go/src/github.com/hyperledger/fabric/fastfabric/scripts/client/data/* /home/ubuntu/BlockProM/log_extraction/data/
cd /home/ubuntu/BlockProM
logdir=$(date +%Y%m%d_%H%M%S)
mkdir -p log_store/$logdir
cp log_extraction/data/* log_store/$logdir
mkdir log_store/$logdir/csv
mkdir log_store/$logdir/csv/keybased
python3 convert_to_csv/fastfabric_convert_blockchain_logs_to_csv.py $logdir
python3 caseid_generation/caseid_generation.py $logdir
python3 metrics_evaluation/metrics_evaluation.py $logdir > log_store/$logdir/optimizationrecommendations.txt

set -ex
