#!/bin/bash

source env.sh
TEST_DURATION_IN_SECONDS=160

PODS=$(kubectl get pods -n $TARGET_NS |  awk '{print $1}' | grep -v NAME)

sleep $TEST_DURATION_IN_SECONDS

mkdir -p .tmp
for p in $PODS
do
   FILE="${p}.pcap"
   kubectl -n $TARGET_NS cp $p:/tmp/tcpdump.pcap ".tmp/${FILE}" -c tcpdumper   
done
./create-capture-metadata.py $TARGET_NS ${PODS}
