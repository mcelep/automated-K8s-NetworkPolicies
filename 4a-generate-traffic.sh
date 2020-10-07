#!/bin/bash

source env.sh
TEST_DURATION_IN_SECONDS=60
kubectl -n $TARGET_NS delete deployment load-generator --ignore-not-found --wait
kubectl -n $TARGET_NS delete pod -l run=load-generator  --wait
sleep 15
PODS=$(kubectl get pods -n $TARGET_NS |  awk '{print $1}' | grep -v NAME)

kubectl -n $TARGET_NS run load-generator --image=${LOAD_GENERATOR_IMAGE} --env=FRONTEND_ADDR=frontend
echo "Going to sleep for $TEST_DURATION_IN_SECONDS"

sleep $TEST_DURATION_IN_SECONDS

mkdir -p .tmp
for p in $PODS
do
   FILE="${p}.pcap"
   kubectl -n $TARGET_NS cp $p:/tmp/tcpdump.pcap ".tmp/${FILE}" -c tcpdumper   
done

#kubectl -n $TARGET_NS delete deployment load-generator  --ignore-not-found
#kubectl -n $TARGET_NS delete pod -l run=load-generator

./4a-create-capture-metadata.py $TARGET_NS ${PODS}

#CAPTURE_META_DATA=".tmp/capture-$(timestamp).log"
#for p in $PODS
#do
#  IP=$(kubectl -n $TARGET_NS get pods $p -o jsonpath='{.status.podIP}{"\n"}')
#  FILE="${p}.pcap"
#  echo "${p} ${FILE} ${IP}">>$CAPTURE_META_DATA
#done

