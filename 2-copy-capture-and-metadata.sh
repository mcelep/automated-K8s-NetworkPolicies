#!/bin/bash

source env.sh

PODS=$(kubectl get pods -n $TARGET_NS |  awk '{print $1}' | grep -v NAME)

i=0

until [ $i -gt $TEST_DURATION_IN_SECONDS ]
do
   echo "Going to wait for $((TEST_DURATION_IN_SECONDS-i)) seconds so that application traffic can be generated..."
  ((i=i+1))
  sleep 1
done


mkdir -p .tmp
for p in $PODS
do
   FILE="${p}.pcap"
   kubectl -n $TARGET_NS cp $p:/tmp/tcpdump.pcap ".tmp/${FILE}" -c tcpdump  
done
./create-capture-metadata.py $TARGET_NS ${PODS}
