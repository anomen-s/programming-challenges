# KUBERNETES_INTRO
* https://github.com/xbendik/kubernetes-1

## Docker
docker tag
docker push

## Alt.
* cri-o
* podman

# K8S
* kubelet
* CNCF
  * k8s
  * prometheus
  * fluentd
* CRI
  * 
* CSI - Container Storage Interface

* Openshift - nadstavba nad K8S

## Nodes
* master node
  * API Server
  * Scheduler
  * Etcd
  * Controller manager
* Worker
  * kubelet - agent pro master node
  * container runtime - docker, ...
  * kube-proxy - networking pro nody

 ## API
* vypsat typy Resources
```
kubectl api-resources
```

 ## Networking
 * pody - pevná IP a DNS
 * Services
  * ClusterIP, NodePort, LoadBalancer

## Namespaces
```
kubectl create ns <namespace>
```

## Persistent Volumes
* PV
* PVC - žádost o PV ze strany podu
  * poskytuje abstrakci mezi konzumenty a poskytovateli uložiště


* DNS: <servicename>.<namespace>.svc.cluster.local

## ClusterIP
* service v rámci clusteru

## NodePort
* naalokuje port (v rozsahu 30000-32000) na každém worker nodu


# Instalace
## docker-desktop
```
kubectl
.kube/config
```

# kubectl

## Cluster Node
```
kubectl get nodes -o wide
kubect describe node docker-desktop
kubectl get cs 
kubectl get all
kubectl config view
```

```
# labely
kubectl label node <node> <klíč>=<label>

# top - zatížení
kubectl top node <node>  

# zakázat/povolit nasazování nových workloadů
kubectl cordon <node>
kubectl uncordon <node>

# evakuovat všechen workload (pody)
kubectl drain <node>

# smazat node
kubectl delete node <node>
```

#  Pody

## Vícekontejnerové
* sdílejí IP a síť
* můžou sdílet další prostředky
* oddělení doplňkových služeb
  * init kontejner
  * sidecar pattern
  * ambassador/adapter paterns

### Init kontejner
* přimo v yamlu initContainers
* spouští se jako první
  * inicializace db
  * stažení secret

## Logy
* stdout
  * Fluentd - export ven (ELK, ...)
  * ztráta logů při záseku nodu
* persistent volume
  * ukládání do PV - potřeba dalšího zpracování

```
kubectl logs -n first-test -l app=nginx -c init
kubectl logs -n first-test -l app=nginx --all-containers=true
```

## Exec
```
kubectl exec -n <ns>  <pod> -i -t -- sh
```

## Liveness a Readiness probes

# Deployment
* spravuje pody

# StatefulSet
* 
# DaemonSet
*  správa běhu podů na definovných nodech

# Job
* jednorázová úloha

# CronJob
* naplánovaná úloha

# Secrets

# Configmap
```
kubectl get cm -n first-test nginx-config -o yaml
kubectl patch cm -n first-test --type merge nginx-config -p '{"data":{"var1":"test value"}}'
kubectl patch cm -n first-test --type merge nginx-config -p '{"data":{"index.html":"<html>ERROR</html>"}}'
kubectl  exec -n first-test  nginx-8f8d8cbcc-28bw7 --  cat /usr/share/nginx/html/test/index.html
```

* vytvořiit z adresáře
```
kubectl create cm konfigurace1 --from-file konfigurace-v1/
```

# HorizontalPodAutoscaler
* automatické škálování

# Ingress

# Istio

# další nástroje
* validace k8s souborů - https://www.fairwinds.com/blog/fairwinds-polaris-kubernetes-open-source-configuration-validation
* CD - Argo CD
* Harbor

# Helm
```
helm install <chart>
helm upgrade <chart>
helm list --all-namespaces
helm pull --untar=true
```
