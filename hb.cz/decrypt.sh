#!/bin/sh

# Decrypt bank statement protected by weak PIN.

if [ -z "$1" ]
then
 echo Missing parameter
 exit 1
fi

/usr/sbin/zip2john $1 > zip.hashes

/usr/sbin/john  --incremental=digits  zip.hashes
