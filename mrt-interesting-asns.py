#!/usr/bin/env python3

import os
import sys
import time
#import json
#import IPy
from datetime import datetime
import re

# When the parent dies we are seeing continual newlines, so we only access so many before stopping
counter = 0
interesting_asns = {}
prefix_file = "aslist.csv"

with open(prefix_file) as fp:
    line = fp.readline()
    while line:
        ## parse line
        parse_me = str(line.rstrip())
        (asnumber, asname) = parse_me.split('|', 2)
        asn = int(asnumber)
        interesting_asns[asn] = asname
        ## fetch another line
        line = fp.readline()

def getSourceASfromASPath(aspathstring):
    if '{' not in aspathstring:
        aspathlist = aspathstring.split(' ')
        sourceasn = aspathlist[-1]
    else:
        aspathstring = re.sub(' \{.*\}$', '', aspathstring)
        aspathlist = aspathstring.split(' ')
        sourceasn = aspathlist[-1]
    return int(sourceasn)

def parseLine(oneline):
    status,srcprefixes,aspath,stuff1,stuff2,stuff3,stuff4,communities,collector,timestamp,stuff5 = oneline.split('|')
    sourceasn = getSourceASfromASPath(aspath)
    if sourceasn in interesting_asns.keys():
        # do stuff
        ts = int(timestamp)
        eventtime = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        prefixes = srcprefixes.split(' ')

        print ("At %s\n  as%d/%s\n  Advertising network(s): %s\n  with AS-PATH: %s" % (eventtime, sourceasn, interesting_asns[sourceasn], prefixes, aspath))

while True:
    try:
        line = sys.stdin.readline().strip()
        if line == "":
            counter += 1
            if counter > 100:
                break
            continue

        counter = 0

        parseLine(line)
    except KeyboardInterrupt:
        pass
    except IOError:
        # most likely a signal during readline
        pass
