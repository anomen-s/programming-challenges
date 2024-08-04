set NS=lhl

kubectl get pods -n %NS%

kubectl logs -n %NS% -l app=nginx -f  
