#!/usr/bin/env python3

from purple.machine import Purple97

purple = Purple97.from_key_sheet(switches='7-7,5,21-12')

plaintext = purple.decrypt("KOROGEBENEAIVZOZEXUOEXNAIIHMUFNABARJI")

print(plaintext)

