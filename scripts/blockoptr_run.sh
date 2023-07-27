#!/usr/bin/env bash

rm -rf log_store

node log_extraction/getBlockchainLogs.js
logdir=$(date +%Y%m%d_%H%M%S)
mkdir -p log_store/$logdir
mv log_extraction/data/* log_store/$logdir/
mkdir log_store/$logdir/csv
mkdir log_store/$logdir/csv/keybased
python3 convert_to_csv/convert_blockchain_logs_to_csv.py $logdir
rm log_store/$logdir/*.json
python3 caseid_generation/caseid_generation.py $logdir
python3 metrics_evaluation/metrics_evaluation.py $logdir > log_store/$logdir/optimizationrecommendations.txt
cat log_store/$logdir/optimizationrecommendations.txt
