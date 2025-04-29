#!/bin/sh

mkdir -p home
export HOME=$(pwd)/home

python3 -m venv venv3
source venv3/bin/activate

pip install rembg --upgrade
pip install onnxruntime --upgrade

python remove-background.py

