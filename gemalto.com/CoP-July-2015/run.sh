#!/bin/sh

echo  65459e07d022a2e1a11c8c307f60397964bc6c64 > /tmp/65459e.txt
/usr/sbin/john --show --format=raw-SHA1 /tmp/65459e.txt

