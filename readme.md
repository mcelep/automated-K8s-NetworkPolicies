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

docker run -t owasp/zap2docker-stable zap-baseline.py -d -t  http://192.168.1.26

TARGET_NS=hipster-shop
PODS=$(kubectl get pods -n $TARGET_NS |  awk '{print $1}' | grep -v NAME)
./4a-create-capture-metadata.py POD

#### translate capture into networkpolicies ####
./5-analyse.py .tmp/capture-2021-02-04_17-15-49.json

namespace=default
cat > tcpdump.yaml << EOF
spec:
  template:
    spec:
      containers:
      - name: tcpdumper
        image: docker.io/dockersec/tcpdump
EOF

########  PATCH Tcpdump to all deployment in namespace X  ########
kubectl get deployment -n $namespace |  awk '{print $1}' | grep -v NAME > deployment.list
declare -a deployment.array=()
a=0
while IFS= read -r line; do    echo $line; kubectl patch deployment $line --patch "$(cat tcpdump.yaml)" ; let "a++"; done < deployment.list

########  PATCH Tcpdump to all deployment in namespace X  ########
kubectl get pods -n $namespace |  awk '{print $1}' | grep -v NAME > pods.list

########  run tcp dump on each pod  #######
while IFS= read -r line; do
     timeout 400 kubectl logs -f $line   -c tcpdumper >  $line.pcap.gz.base64 &
done < pods.list

########  Get Deployment Port/Protocol #######
while IFS= read -r line; do
      kubectl describe deployment  $line  | grep "Port: "  |grep -v Host | grep -F '/' >
done < deployment.list

