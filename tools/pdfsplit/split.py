#!/usr/bin/env python3
import subprocess
import sys
'''
Split pdf using pdftk.
Index file is list of first pages of sections.
Pages are indexed from 1.
Numbers are separated by new-lines.
'''

def run(cmd):
 try:
   result = subprocess.check_output(cmd)
 except subprocess.CalledProcessError as e:
   if e.returncode > 1:
     print (e.output)
     exit(e.returncode)
   return False

 return result.decode("utf-8").strip()



def processFiles(pdfFile, indexFile):
    prev = 1
    sec = 0
    outputFile = pdfFile[0:pdfFile.rfind('.')]
    with open(indexFile, 'r') as f:
      secList = [int(line.strip()) for line in f] + [ 0 ]

    padding = len(str(len(secList)))
    
    for curr in secList:
           if curr > 0:
             prev_end = str(curr - 1)
           else:
             prev_end = 'end'
           params = [
                 'A=' + pdfFile,
                 'cat',
                 'A%i-%s' % (prev, prev_end),
                 'output',
                 '%s-%s.pdf' % (outputFile, str(sec).zfill(padding))]

           print("%i: %i-%s  \t%s" % (sec, prev, prev_end, params), flush=True)

           print(run(['pdftk'] + params))

           sec = sec + 1
           prev = curr

if len(sys.argv) != 3:
  print("Usage: " + sys.argv[0] + " pdfFile indexFile")
else:
  processFiles(sys.argv[1], sys.argv[2])
