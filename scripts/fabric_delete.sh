#!/usr/bin/env bash

set -x


cd ./fabric-samples/test-network
./network.sh down
sleep 10s

set +x
