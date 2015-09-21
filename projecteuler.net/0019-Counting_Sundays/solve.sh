#!/bin/bash


CNT=0

#Sunday is first day of Sept. 1901
cal 9 1901
W1=`cal 9 1901 | head -n 3 | tail -n 1`

for Y in {1901..2000}
do
 for M in {1..12}
 do
  CM=`cal $M $Y | head -n 3 | tail -n 1`
  if [ "x$CM" = "x$W1" ]
  then
   CNT=$((CNT+1))
  fi
  echo $Y $M $CNT
 done
done

echo result=$CNT
