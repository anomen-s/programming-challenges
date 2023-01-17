#!/bin/sh

wget https://github.com/magnumripper/JohnTheRipper/archive/bleeding-jumbo.zip

unzip bleeding-jumbo.zip

cd john-bleeding-jumbo/src

./configure
make -s clean && make -sj4

cd ../run


./pdf2john.pl vypis.pdf > pdf.hash
time ./john --incremental=Digits pdf.hash
