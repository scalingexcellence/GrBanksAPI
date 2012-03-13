#!/usr/bin/python

from alpha import Alpha
from eurobank import Eurobank
from ConfigParser import RawConfigParser
import sys

config = RawConfigParser()

if (len(sys.argv)>1):
    config.readfp(sys.stdin)
else:
    config.read('passwords.cfg')

a = Alpha(config)
e = Eurobank(config)

a.printp()

print "================================================="
e.printp()

print "================================================="
(a+e).printp(True)
