#!/bin/bash

source env.sh

kubectl create ns $TARGET_NS &&

kapp deploy -a hipster-shop -y -f https://raw.githubusercontent.com/yasensim/nsxt-ocp4/master/demo-app.yml -n $TARGET_NS
