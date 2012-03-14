#!/usr/bin/python

import sys
from ConfigParser import RawConfigParser
import grbanks

config = RawConfigParser()

if (len(sys.argv)>1):
    config.readfp(sys.stdin)
else:
    config.read('passwords.cfg')

a = grbanks.Alpha(config)
e = grbanks.Eurobank(config)

a.printp()

print "================================================="
e.printp()

print "================================================="

(a+e).filter(grbanks.FILTER_POSITIVE).printp()
