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

set -x


cd ./fabric-samples/test-network
./network.sh down
./network.sh up createChannel -c mychannel -ca #-s couchdb
./network.sh deployCC -ccn $CHAINCODE_NAME -ccp ~/BlockOptR/chaincodes/$CHAINCODE_NAME$SUFFIX/$PROGRAMMING_LANGUAGE -ccl $PROGRAMMING_LANGUAGE

sleep 10s

set +x

mv ./fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/* ./fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/key_sk
