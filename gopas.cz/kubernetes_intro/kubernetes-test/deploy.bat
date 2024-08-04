docker build -t lhl/nginx:2 .

set NS=lhl

echo %TIME% >> docs/timestamp.txt
kubectl create namespace %NS%

kubectl  apply -n %NS% -f .\configmap.yaml

kubectl delete -n %NS% cm cm-nginx-docdata
kubectl create -n %NS% cm cm-nginx-docdata --from-file docs/

kubectl apply  -n %NS% -f .\secret.yaml

kubectl delete -n %NS% deploy nginx
kubectl apply  -n %NS% -f .\deployment.yaml

kubectl apply  -n %NS% -f .\service.yaml
