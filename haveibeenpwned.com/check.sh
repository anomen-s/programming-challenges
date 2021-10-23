#!/bin/bash

echo Enter password:
read -s P

HASH=`echo -n "$P" | sha1sum`

echo $HASH

PREFIX=`expr substr "$HASH" 1 5`
REST=`expr substr "$HASH" 6 35`

echo checking $PREFIX and $REST:
echo ""
wget https://api.pwnedpasswords.com/range/$PREFIX -q -O - | grep -i $REST

