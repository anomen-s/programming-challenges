#!/usr/bin/env python3
import sys
import re

NUMBER = -1

##
# Convert ":" syntax to proper table for LogXX pages
######

COUNT = 0
TITLE_FOUND = False
HEADER_DONE = False

def line_number():
   global NUMBER, COUNT
   result = NUMBER + COUNT
   COUNT = COUNT + 1
   return result

def printHeader():
    global HEADER_DONE
    if not HEADER_DONE:
        HEADER_DONE = True;
        print('||border="1" style="border-collapse:collapse" cellpadding="5" width="50%"')
        number='číslo'
        date = 'datum'
        name = 'název'
        code = 'kód'
        page = 'stránka'
        comments = 'poznámky'
        print(f'||!{number:<6}||!{date:<10}||!{name:<50}||!{code:<10}||!{page:<12}||!{comments:<20}||')


# TODO: , ''+[[(gcuser:)NAME]],[[(gcuser:)NAME2]]''

def pattern():
 # ':\\s+([0-9.]+)\\s+(.*)\\s*:\\s*([wop]{2}:\\w+)(\\s*\\((\\[\\[\\w+\\]\\])\\))?\s*$'
 DATE='[0-9.]+'
 NAME='(.*)'
 CODE='[wop]{2}:\\w{3,8}'
 PAGE='\\[\\[\\w{3,8}\\]\\]'
 COMM='.*'
 return f"^:\\s+({DATE})\\s+{NAME}\\s*:\\s*({CODE}),?\\s*(?:\\(({PAGE})[\\),]?)?(?:\\s*({COMM}))?$"

def stripBraces(s):
   m = re.match('^\\s*\\((.*)\\)\\s*', s)
   if m:
     return m[1]
   else:
     return s

def checkTitle(line):
   global TITLE_FOUND, NUMBER
   if TITLE_FOUND:
     return
   m = re.match('\\(:title.*\\((\\d+)\\)\\s*:\\)\\s*', line)
   if m:
     TITLE_FOUND = True
     NUMBER = int(m[1]) * 100 - 99


def isHr(line):
   m = re.match('-+\\s*', line)
   return m != None

def format_line(m):
      num = line_number()
      date = m[1]
      name = m[2].strip()
      code = m[3]
      page = m[4] or ' '
      comm = stripBraces(m[5] or ' ')
      return f"||{num:<6} ||{date:<10} ||{name:<50} ||{code:<10} ||{page:12} ||{comm:<20} ||"

def convert_line(line):
    m = re.match(pattern(), line)
    if m != None:
      return format_line(m)
    else:
      return None

def print_empty_lines():
   global COUNT
   while (COUNT < 100):
     l = format_line(['']*10)
     print(l)

def transform(fname):

    with open(fname, 'rt') as f:
       for line in f:
          if checkTitle(line):
             pass
          if isHr(line):
             pass
          else:
            tline = convert_line(line)
            if (tline):
              printHeader()
              print(tline)
            else:
              print(line.strip())
       print_empty_lines()

def finalCheck():
  if not TITLE_FOUND:
    raise Excetion("Page title not generated")
  if not HEADER_DONE:
    raise Excetion("Header not generated")
  if NUMBER < 0:
    raise Excetion("Line number generation failed")

if __name__ == '__main__':
    transform(sys.argv[1])
