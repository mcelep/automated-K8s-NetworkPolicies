#!/bin/bash

source env.sh
TEST_DURATION_IN_SECONDS=30
kubectl -n $TARGET_NS delete deployment load-generator --ignore-not-found --wait
sleep 15
PODS=$(kubectl get pods -n $TARGET_NS |  awk '{print $1}' | grep -v NAME)

kubectl -n $TARGET_NS delete deployment load-generator --ignore-not-found
kubectl -n $TARGET_NS run load-generator --image=${LOAD_GENERATOR_IMAGE} --env=FRONTEND_ADDR=frontend
echo "Going to sleep for $TEST_DURATION_IN_SECONDS"
sleep $TEST_DURATION_IN_SECONDS

mkdir -p .tmp

for p in $PODS
do
   kubectl cp $p:/tmp/tcpdump.pcap ".tmp/${p}.pcap.gz.base64"   -c tcpdumper   
done

kubectl -n $TARGET_NS delete deployment load-generator
