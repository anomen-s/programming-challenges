#!/bin/sh

#XMLLINT_INDENT="	" xmllint --format droid-to-xml.xsl > droid-to-xml.formatted.xsl

FI="$1"

# shift

for YEAR in `seq 2007 2024`
do
 echo -n "$YEAR... "
 SMI="sms-${YEAR}-in.xml"
 SMO="sms-${YEAR}-out.xml"
 mv -f ${SMI} ${SMO} /tmp  2>/dev/null
 echo -n "in "
 xsltproc -o "$SMI" --stringparam TYPE 1 --stringparam YEAR "$YEAR" droid-to-xml.xsl "$FI"
 echo -n "out "
 xsltproc -o "$SMO" --stringparam TYPE 2 --stringparam YEAR "$YEAR" droid-to-xml.xsl "$FI"
 
 for F in "$SMI" "$SMO"
 do 
   WCL=`cat "$F" | wc -l`
   if [ "0$WCL" -lt '04' ]
   then
    echo -n "-"
    rm -f "$F"
   else
    echo -n "+"
   fi
 done
 echo ""

done
 echo -n "Total: "
 grep '<message>' sms-2???-*.xml |wc -l
