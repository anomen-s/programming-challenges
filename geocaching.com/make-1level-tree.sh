#!/bin/sh

for F in GC??*.gpx
do
 PREFIX=`expr $F 1 3`
 echo "$F -> $PREFIX/$F"
 mkdir -p "$PREFIX"
 mv "$F" "$PREFIX/$F"
done
