#!/usr/bin/python

import unicode_excel_write
import urllib, urllib2, cookielib
from decimal import *
from lxml import html
import unicode_excel_write
import code, time
from utils import *

class BaseBank(object):
    
    def __init__(self, name):
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0), #debug
            urllib2.HTTPSHandler(debuglevel=0), #debug
            urllib2.HTTPCookieProcessor(cookielib.CookieJar()) #cookielib.MozillaCookieJar(cookie_filename)
        )
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        self.name = name
        self.__format = FORMAT_DEFAULT
        
    def openUrl(self, url, params=None):
        if params==None:
            g = self.opener.open(url)
        else:
            g = self.opener.open(url, urllib.urlencode(params))
        s = g.read()
        v = html.document_fromstring(s)
        g.close()
        return (s,v)
        
    
    def load(self, user, passw=None, acnt=None):
        (self.left, self.table) = self._load(user, passw, acnt)
        self.left = Decimal(self.left)
        self.table = map(lambda s: {'date':s[0], 'name':s[1], 'amount':Decimal(s[2]), 'description':s[3]}, self.table)
        
    def manage_up(self, user, passw, acnt):
        if passw==None:
            # in this case the first argument is a configuration file
            passw=user.get(self.name,'pass')
            acnt=user.get(self.name,'acnt')
            user=user.get(self.name,'user')
        return (user, passw, acnt)
        
    def toCsv(self, filename):
        fo = open(filename, 'wb')
        g = unicode_excel_write.UnicodeWriter(fo)
        g.writerow(['date','account','amount','description'])
        g.writerows([self.__format(row) for row in self.table])
        g.writerow(["total: ","",self.__format(self.left, Type.CURRENCY)])
        fo.close()
        return self
    
    def printp(self):
        print "\n".join(["%s %s %12s %s" % self.__format(row) for row in self.table]).encode('utf-8')
        print "-------------------------------------------------"
        print "                                  total: %4s" % self.__format(self.left, Type.CURRENCY)
        return self
        
    def __clone(self):
        b = BaseBank(self.name)
        b.__format = self.__format
        b.left = self.left
        b.table = self.table
        return b

    def format(self, format=FORMAT_DEFAULT):
        b = self.__clone()
        b.__format = format
        return b
        
    def filter(self, filter=FILTER_ALL):
        b = self.__clone()
        b.table = [row for row in b.table if filter(row)]
        return b
    
    def __add__(self, other):
        b = BaseBank("%s_%s"%(self.name,other.name))
        b.__format = self.__format
        b.left = self.left+other.left
        b.table = sorted(self.table+other.table, key=lambda s: s['date'])
        return b
