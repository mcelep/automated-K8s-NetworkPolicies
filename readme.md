#  Microsegmanservice

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
kapp apply -f demo-app.yaml

#### patch tcpdump on the PODS in TARGET_NS ####
./activate_dump 

#### generate Traffic ####
docker run -t owasp/zap2docker-stable zap-baseline.py -d -t  http://192.168.1.26

#### analysse ####
./5-analyse.py .tmp/capture-2021-02-10_10-01-00.json 

#### apply policies ####
 kubectl apply -f .tmp/network-policies/ -n hipster-shop
