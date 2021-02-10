#  K8s AutoSegmant

 **##### the begining 
```diff
This project contains a script that can automate networkpolicies creation based on the application traffic.
the scripts is doing the following: 
1) Patch Wirdshark sidecar for namespace
2) capture traffic
3) convert/parse tcpdump capture into log
4) convert log to networkpolocie json format


 **##### network poclicies
```diff

the git is still under construction

# instruction

#### Deploy App ####
TARGET_NS=hipster-shop
kapp apply -f demo-app.yaml -n hipster-shop



#### patch tcpdump on the PODS in TARGET_NS ####
1-inject-sidecar.sh 

#### activate dump #### 

./2-activate_dump.sh

#### generate Traffic (you have 160 sec timeout as default) ####

docker run -t owasp/zap2docker-stable zap-baseline.py -d -t  http://192.168.1.26

#note: the traffic generator skipped the checkout service , please add cart manualy during the capture (http://192.168.1.26/cart/checkout)

#### analysse ####
./5-analyse.py .tmp/capture-2021-02-10_10-01-00.json 

#### apply policies ####
 kubectl apply -f .tmp/network-policies/ -n hipster-shop
 
 
#### lets test it with the wrong label ####

#### POD with label app=frontend trying to access the checkout service

kubectl run test-$RANDOM --labels=app=frontend  --namespace=hipster-shop --rm -i -t --image=alpine -- sh
If you don't see a command prompt, try pressing enter.
/ # nc -zv 100.96.1.42 5050
100.96.1.42 (100.96.1.42:5050) open
 
#### POD with label app=wrong trying to access the checkout service

kubectl run test-$RANDOM --labels=app=wrong  --namespace=hipster-shop --rm -i -t --image=alpine -- sh
If you don't see a command prompt, try pressing enter.
/ # nc -zv 100.96.1.23 5050
nc: 100.96.1.23 (100.96.1.23:5050): Host is unreachable

