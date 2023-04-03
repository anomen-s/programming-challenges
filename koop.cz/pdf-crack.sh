#!/bin/sh


PDF=vypis.pdf

if [ ! -e target/$PDF ]
then
 echo target/$PDF not found
 exit 1
fi

cd target

./john-bleeding-jumbo/run/pdf2john.pl $PDF > pdf.hash

time python3 ../rcgen.py | ./john-bleeding-jumbo/run/john --pipe pdf.hash

