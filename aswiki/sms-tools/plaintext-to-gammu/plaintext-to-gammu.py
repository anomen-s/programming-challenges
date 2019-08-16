#!/usr/bin/env python3
import sys
import re

DIRECTION = 'Read'
#DIRECTION = 'Sent'

class Record:
    pass

def printRecord(r):
  if r:
    print('  <message>');
    print('    <date>'+r.date+'</date>');
    print('    <dateenc>'+r.dateenc+'</dateenc>');
    print('    <text>'+r.text+'</text>');
    print('    <telephone>'+r.telephone+'</telephone>');
    print('    <contact>'+r.contact+'</contact>');
    print('    <stat>'+DIRECTION+'</stat>');
    print('  </message>');

def parseHeader(line, text):
    p = re.compile('>\s+([0-9/-]+)[ T]\s*([Z0-9:]+)\s+"?([+]?\d+)?"?\s*(.*)?')
    m = p.match(line);
    if not m:
      raise Exception("invalid line: " + line)
    r = Record();
    parseDateTime(r, m.group(1), m.group(2));
    r.text = text;
    r.telephone = m.group(3) or '';
    r.contact = m.group(4) or '';
    return r;

def parseDateTime(r, date, time):
    d = None
    t = None

    # YYYYmmdd
    cymd = re.compile('(\d{4})(\d{2})(\d{2})')
    m = cymd.match(date)
    if m:
      d = m.group(3) + '.' + m.group(2) + '.' + m.group(1);
      dateenc = m.group(1) + d2(m.group(2)) + d2(m.group(3));
    
    # YYYY-mm-dd
    ymd = re.compile('(\d{4})-(\d{1,2})-(\d{1,2})')
    m = ymd.match(date)
    if m:
      d = m.group(3) + '.' + m.group(2) + '.' + m.group(1);
      dateenc = m.group(1) + d2(m.group(2)) + d2(m.group(3));
    
    # dd/mm/yy
    dmy = re.compile('(\d{2})/(\d{1,2})/(\d{1,2})')
    m = dmy.match(date)
    if m:
      d = m.group(1) + '.' + m.group(2) + '.' + toYear(m.group(3));
      dateenc = toYear(m.group(3)) + d2(m.group(2)) + d2(m.group(1));

    if not d:
      raise Exception('Invalid date: ' + date)

    # HHMMSS
    chms = re.compile('(\d{2})(\d{2})(\d{1,2})Z')
    m = chms.match(time)
    if m:
      t = m.group(1) + ':' + m.group(2) + ':' + m.group(3);
      timeenc =  d2(m.group(1)) + d2(m.group(2)) + m.group(3);
      
    # HH:MM:SS
    hms = re.compile('(\d{1,2}):(\d{1,2})(:(\d{1,2}))?')
    m = hms.match(time)
    if m:
      t = m.group(1) + ':' + m.group(2) + ':' + (m.group(4) or '00');
      timeenc =  d2(m.group(1)) + d2(m.group(2)) + (m.group(4) or '00');

    if not t:
      raise Exception('Invalid time: ' + time);

    r.date = d + ' ' + t;
    r.dateenc = dateenc + timeenc;

def toYear(y):
    if len(y) == 2:
      return ('20' + y) if (y[0] < '8') else ('19' + y);
    return y;

def d2(value):
    if len(value) == 1:
      return '0' + value;
    return value;

def appendText(text, line):
    l = line.strip();
    if text:
      text = text + '<br/>' + l;
    else:
      text = l;
    return text;

def main():
    print('<?xml version="1.0" encoding="utf-8"?>');
    print('<?xml-stylesheet type="text/xsl" href="sms.xsl"?>');
    print('<messages>');

    with open(sys.argv[1], 'rt') as f:
      lines = f.readlines();
      text = None;
      for line in lines:
        if (line != ''):
         if (line[0] == '>'):
            r = parseHeader(line, text);
            printRecord(r);
            text = None;
         else:
            text = appendText(text, line);
    print('</messages>');

main();
