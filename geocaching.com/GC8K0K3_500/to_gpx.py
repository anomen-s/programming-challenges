#!/usr/bin/env python3
import re
import html
import sys


'''
Create GPX from https://jirkasta.cz/mapa-500/
'''

GCCODE="GC8K0K3"

FILE_HEADER="""<?xml version="1.0" encoding="utf-8"?>
<gpx
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns:groundspeak="http://www.groundspeak.com/cache/1/0/1"
  version="1.0"
  xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd http://www.groundspeak.com/cache/1/0/1 http://www.groundspeak.com/cache/1/0/1/cache.xsd"
  creator="python3"
  xmlns="http://www.topografix.com/GPX/1/0">
  <name>%GCCODE%</name>
"""

FILE_TRAILER="\n</gpx>\n"


TEMPLATE="""
  <wpt lat="%LAT%" lon="%LON%">
    <time>2023-01-24T00:00:00</time>
    <name>%GCCODE%%SEQNAME%</name>
    <desc>%NAME%, %CONTAINER% Cache (%DIF%/%TER%)</desc>
    <url>https://coord.info/%GCCODE%</url>
    <urlname>%NAME%</urlname>
    <sym>Geocache</sym>
    <type>Geocache|%TYPE%</type>
    <groundspeak:cache id="8950457" archived="False" available="True">
      <groundspeak:name>%NAME%</groundspeak:name>
      <groundspeak:placed_by>Routparta</groundspeak:placed_by>
      <groundspeak:owner id="43772795">Routparta</groundspeak:owner>
      <groundspeak:type>%TYPE%</groundspeak:type>
      <groundspeak:container>%CONTAINER%</groundspeak:container>
      <groundspeak:difficulty>%DIF%</groundspeak:difficulty>
      <groundspeak:terrain>%TER%</groundspeak:terrain>
      <groundspeak:country>Czechia</groundspeak:country>
      <groundspeak:state>Hlavní město Praha</groundspeak:state>
      <groundspeak:short_description html="True">
      </groundspeak:short_description>
      <groundspeak:long_description html="True">%DESCR%</groundspeak:long_description>
    </groundspeak:cache>
  </wpt>
"""

MAPPING={
"7": "Earthcache",
"3": "Letterbox Hybrid",
"Event Cache": "Event Cache",
"2": "Multi-cache",
"5": "Traditional Cache",
"1": "Unknown Cache",
"4": "Wherigo Cache",
"10": "Unknown Cache", # checked flag
"12": "Virtual cache",
"8": "Virtual cache",
"9": "Webcam Cache",
"11": "Locationless (Reverse) Cache",
"Mikro": "Micro",
"Jiná": "Other",
"Not chosen": "Not chosen"
}

def M(value):
  if value in MAPPING:
    return MAPPING[value]
  else:
    return value

def read_input():
  fname = 'index.html'
  if len(sys.argv) > 1:
   fname = sys.argv[1]

  with open(fname, 'rt') as f:
    for line in f:
      if line[0] == '[':
        return eval(line)
  raise Exception("Parsing failed")


def parse_point(seq, p):
  print(p)
  ter = "1.0"
  dif = "1.0"
  cont = "Other"
  cache_type = p[3]
  name=p[5].split("<")[0]
  match = re.compile('Obtížnost:\\s+([0-9,]+)').search(p[5])
  if match:
    dif = match[1].replace(',','.')

  match = re.compile('Terén:\\s+([0-9,]+)').search(p[5])
  if match:
    ter = match[1].replace(',','.')

  match = re.compile('Velikost:\\s+(\\w+)').search(p[5])
  if match:
    cont = match[1].replace(',','.')

  return TEMPLATE \
    .replace("%GCCODE%", GCCODE) \
    .replace("%SEQNAME%", "%02i" % seq) \
    .replace("%DESCR%", html.escape(p[5])) \
    .replace("%TER%", ter)  \
    .replace("%TYPE%", M(cache_type))  \
    .replace("%DIF%", dif)  \
    .replace("%CONTAINER%", M(cont)) \
    .replace("%NAME%", html.escape(name))  \
    .replace("%LAT%", p[1].replace("+","")) \
    .replace("%LON%", p[2].replace("+","")) \



def to_gpx(points):
  
  with open("output.gpx", 'wt') as f:
    f.write(FILE_HEADER.replace("%GCCODE%", GCCODE))

    for p in enumerate(points):
      f.write(parse_point(*p))

    f.write(FILE_TRAILER)


def main():
  data = read_input()
  # print(data)
  to_gpx(data)

if __name__ == '__main__':
   main()
