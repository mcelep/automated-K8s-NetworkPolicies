#!/bin/bash

source env.sh

rm -rf .tmp
git clone https://github.com/GoogleCloudPlatform/microservices-demo.git .tmp/microservices-demo

docker build .tmp/microservices-demo/src/loadgenerator  --tag "${LOAD_GENERATOR_IMAGE}"
docker push "${LOAD_GENERATOR_IMAGE}"
