
for A in "`ls -d 0*\ *`"
do
 NA=`echo "$A" | tr ' ' '_'`
 mv -v "$A" "$NA"
done
