# BlockProM : Steps for log extraction
rm log_extraction/data/*
kubectl cp log_extraction hlf-peer--org1--peer0-0:./
kubectl exec -it hlf-peer--org1--peer0-0 -- /bin/sh
cd log_extraction/
apk update
apk add npm
npm install
node getBlockchainLogs.js
exit
kubectl cp -c peer hlf-peer--org1--peer0-0:data log_extraction/data/.
mkdir -p log_store/$(date +%Y%m%d_%H%M%S) && cp log_extraction/data/* $_
