#!/usr/bin/python
#
# Get daily mileages from JogNote in JSON format
#
from urllib.request import urlopen
import datetime
import getopt
import json
import re
import sys
import xml.etree.ElementTree as ET

def usage():
    print('usage: python jognote.py uid start_date [end_date]', file=sys.stderr)

def cmp_date(a, b):
    cmp = a[0] - b[0]
    if cmp != 0: return cmp
    cmp = a[1] - b[1]
    if cmp != 0: return cmp
    return a[2] - b[2]

def parse_date(str):
    d = str.split('-')
    d[0] = int(d[0])
    d[1] = int(d[1])
    if len(d) <= 2:
        d += [ None ]
    else:
        d[2] = int(d[2])
    return d

def main():
    args = sys.argv[1:]

    if len(args) != 2 and len(args) != 3:
        usage()
        sys.exit(1)

    uid = args[0]
    try:
        s = parse_date(args[1])
    except:
        print("Could not parse start_date: " + args[1])
        sys.exit(1)
    if len(args) == 3:
        try:
            e = parse_date(args[2])
        except:
            print("Could not parse end_date: " + args[1])
            sys.exit(1)
    else:
        e = s

    s = [s[0], s[1], s[2] if not s[2] is None else 1]
    e = [e[0], e[1], e[2] if not e[2] is None else 31]
    c = s
    r = {}
    while cmp_date(c, e) <= 0:
        xml = urlopen(('http://www.jognote.com/user/{uid}/jogs?' +
            'cycle=daily&month={month}&year={year}&format=xml').format(
            uid=28041, year=c[0], month=c[1])).read()
        root = ET.fromstring(xml)
        graphs = root.find('graphs')[1]
        for i, x in enumerate(root.find('series')):
            if graphs[i].text is None:
                continue
            dt = datetime.datetime.strptime(x.text, '%y/%m/%d')
            if cmp_date([dt.year, dt.month, dt.day], e) > 0:
                break
            r[datetime.datetime.strftime(dt, '%Y-%m-%d')] = \
                float(graphs[i].text)
        if c[1] == 12:
            c[0] = c[0] + 1
            c[1] = 1
        else:
            c[1] = c[1] + 1

    print(json.dumps(r))

if __name__ == '__main__':
    main()
