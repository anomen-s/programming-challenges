#!/bin/sh

#XMLLINT_INDENT="	" xmllint --format  xml-fix-sort.xsl >  xml-fix-sort.formatted.xsl
#XMLLINT_INDENT="	" xmllint --format  xml-fix-add-date.xsl >  xml-fix-add-date.formatted.xsl

FI="$1"
#FI=test.xml

cat "$FI" | xsltproc xml-fix-add-date.xsl - | xsltproc xml-fix-sort.xsl - | xmllint --format --encode utf-8 - > "${FI}.fixed.xml"
