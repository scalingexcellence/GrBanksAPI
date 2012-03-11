#!/usr/bin/python

from alpha import Alpha
from eurobank import Eurobank
from ConfigParser import RawConfigParser

config = RawConfigParser()
config.read('passwords.cfg')

a = Alpha(config)
e = Eurobank(config)

a.printp()

print "================================================="
e.printp()

print "================================================="
(a+e).printp()
