#!/usr/bin/env bash

if [ $# -ne 2 ] ; then
    echo "usage: reset_network.sh <chaincode_name> <programming_language>"
    exit 2
fi

CHAINCODE_NAME="$1"

PROGRAMMING_LANGUAGE="$2"

if [ ! -d  chaincodes/$CHAINCODE_NAME ] ; then
    echo "ERROR: Invalid chaincode folder name"
    exit 0
fi

SUFFIX=""

if [ "$2" == "javascript" ] ; then
    SUFFIX="/node"
fi


cd  ~/BlockOptR/workloads/$CHAINCODE_NAME
npm install

cd  ~/BlockOptR
npx caliper launch manager --caliper-workspace ./ --caliper-networkconfig log_extraction/connectionprofile.yaml --caliper-benchconfig workloads/$CHAINCODE_NAME/config.yaml --caliper-flow-only-test --caliper-fabric-gateway-enabled --caliper-fabric-timeout-invokeorquery 110

set +x
