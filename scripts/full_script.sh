#!/usr/bin/env bash
set +ex

#This script assumes that the Fabric network was setup with HyperledgerLab2 testbed. Modifiy this script accordingly to match other deployments of Fabric

chaincode=$1
expnum=$2

rm log_extraction/data/*

kubectl exec hlf-peer--org1--peer0-0 -- sh -c "rm -rf log_extraction"
kubectl exec hlf-peer--org1--peer0-0 -- sh -c "rm -rf node_modules"
kubectl cp log_extraction hlf-peer--org1--peer0-0:./
kubectl exec hlf-peer--org1--peer0-0 -- sh -c "apk update"
kubectl exec hlf-peer--org1--peer0-0 -- sh -c "apk add g++ make py3-pip"
kubectl exec hlf-peer--org1--peer0-0 -- sh -c "apk add npm"
kubectl exec hlf-peer--org1--peer0-0 -- sh -c "npm i fabric-client"
kubectl exec hlf-peer--org1--peer0-0 -- sh -c "node log_extraction/getBlockchainLogs.js"
kubectl cp -c peer hlf-peer--org1--peer0-0:log_extraction/data log_extraction/data/.
kubectl exec hlf-peer--org1--peer0-0 -- sh -c "rm -rf log_extraction"
kubectl exec hlf-peer--org1--peer0-0 -- sh -c "rm -rf node_modules"
logdir=$(date +%Y%m%d_%H%M%S)
mkdir -p log_store/$logdir
#mkdir log_store/$logdir/json
mv log_extraction/data/* log_store/$logdir/
rm log_extraction/data/*
mkdir log_store/$logdir/csv
mkdir log_store/$logdir/csv/keybased
python3 convert_to_csv/convert_blockchain_logs_to_csv.py $logdir
rm log_store/$logdir/*.json
python3 caseid_generation/caseid_generation.py $logdir
python3 metrics_evaluation/metrics_evaluation.py $logdir > log_store/$logdir/optimizationrecommendations.txt
mkdir log_store/$logdir/configfiles
cp /home/ubuntu/HyperLedgerLab-2.0_Extended/caliper/benchmarks/$chaincode/config.yaml log_store/$logdir/configfiles/
cp /home/ubuntu/HyperLedgerLab-2.0_Extended/fabric/network-configuration.yaml log_store/$logdir/configfiles/
cp /home/ubuntu/HyperLedgerLab-2.0_Extended/terraform/cluster.tfvars log_store/$logdir/configfiles/
cp /home/ubuntu/HyperLedgerLab-2.0_Extended/caliper/caliper-config/templates/networkConfig.yaml log_store/$logdir/configfiles/
cp /home/ubuntu/HyperLedgerLab-2.0_Extended/fabric/config/templates/configtx.yaml log_store/$logdir/configfiles/
kubectl logs -f $(kubectl get pods | awk '/manager/ {print $1;exit}') > log_store/$logdir/configfiles/caliper_logs.txt
cp /home/ubuntu/HyperLedgerLab-2.0_Extended/caliper/benchmarks/generator/getParameters.js log_store/$logdir/configfiles/
cp /home/ubuntu/HyperLedgerLab-2.0_Extended/caliper/benchmarks/generator/random.js log_store/$logdir/configfiles/
rm log_extraction/data/*
rm log_store/$logdir/*.json

printf "%.2f," $(grep '| common' log_store/$logdir/configfiles/caliper_logs.txt | awk '{print $4}' | tail -n 2) >> log_store/$logdir/csv/tempmetricslog.csv
printf "%.2f," $(grep '| common' log_store/$logdir/configfiles/caliper_logs.txt | awk '{print $6}' | tail -n 2) >> log_store/$logdir/csv/tempmetricslog.csv
printf "%.2f," $(grep '| common' log_store/$logdir/configfiles/caliper_logs.txt | awk '{print $8}' | tail -n 2) >> log_store/$logdir/csv/tempmetricslog.csv
printf "%.2f," $(grep '| common' log_store/$logdir/configfiles/caliper_logs.txt | awk '{print $14}' | tail -n 2) >> log_store/$logdir/csv/tempmetricslog.csv
printf "%.2f," $(grep '| common' log_store/$logdir/configfiles/caliper_logs.txt | awk '{print $16}' | tail -n 2) >> log_store/$logdir/csv/tempmetricslog.csv

python3 metrics_evaluation/extractcalipermetrics.py $logdir $expnum
python3 metrics_evaluation/extractmetrics.py $logdir $expnum

set -ex
