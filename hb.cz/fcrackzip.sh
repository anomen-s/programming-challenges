#!/bin/sh

# Decrypt bank statement protected by weak PIN.

if [ -z "$1" ]
then
 echo "Missing parameter (zip file)"
 exit 1
fi

fcrackzip  --charset 1 --length 3-9  --brute-force  --verbose "$1"
