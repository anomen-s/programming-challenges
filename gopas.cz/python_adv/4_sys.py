#!/usr/bin/env python3

import sys
import os

print(sys.argv)

print('-' * 30)

print(*[(v, os.environ[v]) for v in os.environ], sep='\n')
