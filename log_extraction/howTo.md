# BlockProM : Steps for log extraction
1. rm log_extraction/data/*

2. kubectl cp log_extraction hlf-peer--org1--peer0-0:./

3. kubectl exec -it hlf-peer--org1--peer0-0 -- /bin/sh

4. cd log_extraction/

5. apk update

6. apk add npm

7. npm install

8. node getBlockchainLogs.js

9. exit

10. kubectl cp -c peer hlf-peer--org1--peer0-0:data log_extraction/data/.

11. mkdir -p log_store/$(date +%Y%m%d_%H%M%S) && cp log_extraction/data/* $_
