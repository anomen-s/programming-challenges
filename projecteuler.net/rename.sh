
ls -d 0*\ * | while read F
do
 echo $F
 NA=`echo "$F" | tr ' ' '_'`
 mv -v "$F" "$NA"
done

