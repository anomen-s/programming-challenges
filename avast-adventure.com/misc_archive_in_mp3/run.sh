#!/bin/sh

mkdir -p target
cd target

wget https://github.com/avast/ctf-aca-brno-2020/raw/master/misc_archive_in_mp3/carrier.mp3

binwalk -e carrier.mp3

bunzip2 < _carrier.mp3.extracted/flag.bz2
