#!/usr/bin/env bash
set +ex

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
mkdir -p log_store/$logdir && cp log_extraction/data/* log_store/$logdir
rm log_extraction/data/*

set -ex
