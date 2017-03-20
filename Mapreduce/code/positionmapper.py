#!/usr/bin/python
import sys
for line in sys.stdin:
    line = line.strip()
    line = line.split(',')
    if int(line[9]) & 0x00FFFFFF != 0:
        print "%s\t%s\t%s\t%s\t%s" % (line[2], line[3], line[6], line[7], (int(line[9]) & 0x00FFFFFF)/1000)