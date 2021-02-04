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
kapp deploy -a hipster-shop -y -f https://raw.githubusercontent.com/yasensim/nsxt-ocp4/master/demo-app.yml -n $TARGET_NS

#### patch tcpdump on the PODS in TARGET_NS ####
./2-inject-sidecar.sh 

#### patch tcpdump on the PODS in TARGET_NS ####
./4a-generate-traffic.sh


TARGET_NS=hipster-shop
PODS=$(kubectl get pods -n $TARGET_NS |  awk '{print $1}' | grep -v NAME)
/4a-create-capture-metadata.py 

#### translate capture into networkpolicies ####
./5-analyse.py .tmp/capture-2021-02-04_17-15-49.json
