#!/bin/sh

mkdir -p target
cd target

wget https://github.com/avast/ctf-aca-brno-2020/raw/master/misc_corrupted_header/corrupt.pmg

patch < ../header.patch

mv corrupt.pmg corrupt.png
