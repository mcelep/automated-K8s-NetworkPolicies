#  Microsegmanservice

 **##### the begining 
```diff
lets start here
```


 **##### network poclicies
```diff

In the following example, incoming traffic to pods with label app=db are allowed only if they come from a pod with app=web, on port 80.


kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-same-namespace
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: db
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: web
    ports:
      - port: 80
      
```
