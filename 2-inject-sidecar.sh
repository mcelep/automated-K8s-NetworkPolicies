#!/bin/bash

source env.sh
DEPLOYMENTS=$(kubectl get deployment -n $TARGET_NS -o name)

for d in $DEPLOYMENTS
do
  #kubectl -n $TARGET_NS patch $d --patch "$(cat tshark-sidecar-patch.yaml)" 
  kubectl -n $TARGET_NS patch $d --patch "$(cat tcpdumper-sidecar-patch.yaml)" 
done
