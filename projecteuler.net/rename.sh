
ls -d 0*\ * | while read F
do
 echo $F
 NA=`echo "$F" | tr ' ' '_'`
 git mv -v "$F" "$NA"
 mv -v "$F" "$NA"
done

