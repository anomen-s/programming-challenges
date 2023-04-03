#!/bin/sh

mkdir -p target
cd target

wget https://github.com/magnumripper/JohnTheRipper/archive/bleeding-jumbo.zip

unzip bleeding-jumbo.zip

cd john-bleeding-jumbo/src

./configure
make -s clean && make -sj4

