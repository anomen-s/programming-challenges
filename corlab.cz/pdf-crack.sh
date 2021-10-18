#!/bin/sh

wget https://github.com/magnumripper/JohnTheRipper/archive/bleeding-jumbo.zip

unzip bleeding-jumbo.zip

cd john-bleeding-jumbo/src

./configure
make -s clean && make -sj4

cd ../run


# john.conf:
## [Incremental:ASCII]
## MaxLen = 5


./pdf2john.pl Corlab_Certificate.pdf > pdf.hash
./john pdf.hash
