#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

#__package__   = 'wptsplit'
__version__   = '1.0'
__author__    = 'anomen, based on http://wiki.samat.org/GpxSplitter by Samat K Jain <samat@samat.org>'
__url__       = 'https://github.com/anomen-s/programming-challenges/tree/master/geocaching.com/wptsplit.py'
__copyright__ = 'Copyright (c) 2021 anomen'
__license__   = 'GPL v3'

import collections
import copy
import os
import pprint
import time

import dateutil.parser

from lxml import etree

TrackTuple = collections.namedtuple(
    'TrackTuple',
    ['track_etree',
     'num_points',
     'bounding_box',
     'waypoints',
     'start_date',
     'end_date'
    ])


def determineBoundingBox(points):
    """Determine the bounding box of a set of points.
    """
    # This is slow. But works correctly.
    lats = [p.attrib['lat'] for p in points]
    lons = [p.attrib['lon'] for p in points]

    lats.sort()
    lons.sort()

    r = {}
    r['minlat'], r['maxlat'] = lats[0], lats[-1]

    # Because we things kept as strings, sort is lexical instead of
    # numeric. Negative numbers were sorted in reverse
    r['minlon'], r['maxlon'] = lons[-1], lons[0]

    return r


def getWptName(wpt, ns):
    for el in wpt:
      if el.tag == "{%s}name" % ns:
        return el.text
    return None

def getState(wpt):
    GS_NS = "http://www.groundspeak.com/cache/1/0"
    elems = document.findall('//{%s}cache/{%s}state' % (GS_NS, GS_NS))
    for el in elems:
        return el.text.replace(' ','_')
    return ''

def getCacheName(wpt):
    GS_NS = "http://www.groundspeak.com/cache/1/0"
    elems = document.findall('//{%s}cache/{%s}name' % (GS_NS, GS_NS))
    for el in elems:
        return el.text.replace(' ','_')
    return ''

def go(document):
    # Detect whether GPX 1.0 or 1.1 is in use
    gpx_ns = document.xpath('namespace-uri(.)')
    gpx_namespaces = ['http://www.topografix.com/GPX/1/0',
                      'http://www.topografix.com/GPX/1/1']

    # FIXME: Turn this into an exception
    if gpx_ns not in gpx_namespaces:
        print >> sys.stderr, 'Unable to determine GPX version (neither 1.0 or 1.1)' % prog_name
        sys.exit(1)

    waypoints = document.findall('//{%s}wpt' % gpx_ns)
    

    for wp in waypoints:
        document = etree.XML('''\
         <gpx xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            version="1.0" creator="Groundspeak"
            xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd http://www.groundspeak.com/cache/1/0 http://www.groundspeak.com/cache/1/0/cache.xsd"
            xmlns="http://www.topografix.com/GPX/1/0">
         </gpx>
        ''')
        wptname = getWptName(wp, gpx_ns)
        nameel = etree.Element("{%s}name" % gpx_ns)
        nameel.text = wptname
        document.append(nameel)
        document.append(wp)

        filename = wptname #  + '-' + ''.join(filter(str.isalnum, getCacheName(wp)))
        print(filename)
        #print(etree.tostring(wp)[0:180])

        data = etree.tostring(document, encoding='UTF-8', xml_declaration=True)
        #tree.tostring(document)
        #document.write(sys.stdout, pretty_print=True)
        with open('%s.gpx' % filename, 'wb') as f: # append to file; use with to have file closed automatically
           f.write(data) # write data to file
        #document.write("%s.gpx" % wptname, xml_declaration=True, encoding="UTF-8", pretty_print=True)

    return


if __name__ == '__main__':
    import sys

    prog_name = os.path.basename(sys.argv[0])

    try:
        for ext in ['', '.gpx', '.GPX']:
            try:
                file_name = sys.argv[1] + ext
                document = etree.parse(file_name)
                break
            except IOError:
                print('Input file not found: %s' % file_name, file=sys.stderr)

        go(document)

    except (NameError, IndexError):
        print('Usage: %s filename.gpx' % prog_name, file=sys.stderr)
        sys.exit(1)
