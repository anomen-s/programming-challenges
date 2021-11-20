#!/bin/sh

for F in GC??*.gpx
do
 PREFIX1=`expr substr "$F" 1 3`
 PREFIX2=`expr substr "$F" 1 4`
 echo "$F -> $PREFIX1/$PREFIX2/$F"
 mkdir -p "$PREFIX1/$PREFIX2"
 mv "$F" "$PREFIX1/$PREFIX2/$F"
done
