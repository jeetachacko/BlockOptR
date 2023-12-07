#!/usr/bin/env bash

if [ $# -ne 2 ] ; then
    echo "usage: reset_network.sh <chaincode_name> <programming_language>"
    exit 2
fi

CHAINCODE_NAME="$1"

sed -i "10s/.*/    - id: $CHAINCODE_NAME/" /home/ubuntu/BlockOptR/networks/networkConfig.yaml


PROGRAMMING_LANGUAGE="$2"

CHAINCODE_FOLDER="chaincodes/$CHAINCODE_NAME/$PROGRAMMING_LANGUAGE"

SUFFIX=""

if [ "$2" == "javascript" ] ; then
    SUFFIX="/node"
    CHAINCODE_FOLDER="chaincodes/$CHAINCODE_NAME/node"
    #CHAINCODE_NAME=$1$SUFFIX
fi

if [ ! -d  $CHAINCODE_FOLDER ] ; then
    echo "ERROR: Invalid chaincode folder name"
    exit 0
fi


set -x

source ~/.bashrc
source ~/.profile

cd ./fabric-samples/test-network
./network.sh down
./network.sh up createChannel -c mychannel -ca #-s couchdb
./network.sh deployCC -ccn $CHAINCODE_NAME -ccp ~/BlockOptR/$CHAINCODE_FOLDER -ccl $PROGRAMMING_LANGUAGE

sleep 10s

set +x

cd ~/BlockOptR

mv ./fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/* ./fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/key_sk
