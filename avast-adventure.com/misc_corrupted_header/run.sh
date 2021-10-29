#!/bin/sh

mkdir -p target

cp corrupt.pmg target/

cd target
patch < ../header.patch

mv corrupt.pmg corrupt.png
