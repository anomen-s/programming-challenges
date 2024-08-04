if "%1%" NEQ "" (
 kubectl  exec -n lhl %1%   -i -t  --  sh
 exit 1
)

kubectl get pods -n lhl
