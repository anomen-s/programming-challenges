#!/bin/sh

mkdir -p target
cd target

wget https://github.com/avast/ctf-aca-brno-2020/raw/master/misc_jpg_metadata/vlcek.jpg

exiftool vlcek.jpg
