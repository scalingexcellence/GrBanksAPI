#!/usr/bin/python
# -*- coding: utf-8 -*-

from basebank import BaseBank

import time

class Eurobank(BaseBank):
    def __init__(self, user=None, passw=None, acnt=None, name="EUROB"):
        super(Eurobank, self).__init__(name)
        if user!=None: self.load(user,passw,acnt)
    
    def _load(self, user, passw=None, acnt=None):
        (user,passw,acnt)=self.manage_up(user,passw,acnt)
    
        (s,v)=self.openUrl('https://ebanking.eurobank.gr/ebanking/login.faces')
        
        action = v.xpath("//form[@id='main']/@action")[0] #Will be something like: /ebanking/login.faces;jsessionid=xxx
        ViewState = [g.attrib['value'] for g in v.xpath("//form[@id='main']//input") if g.attrib['name']=='javax.faces.ViewState'][0]

        params = {
            "main":"main",
            "j_username": user,
            "j_password": passw,
            "login": u"\u0395\u03af\u03c3\u03bf\u03b4\u03bf\u03c2".encode( "utf-8" ),
            "javax.faces.ViewState":ViewState
        }

        (s,v)=self.openUrl('https://ebanking.eurobank.gr'+action, params)

        (s,v)=self.openUrl("https://ebanking.eurobank.gr/ebanking/cashmanagement/accounts.faces?n=%s&ic=1"%acnt)

        left = v.xpath('//table[@class="fldgrp lft cash"]/tbody/tr[4]/td[2]/text()')[0].replace(',','.')
        
        date = [time.strptime(g,'%d/%m/%Y') for g in v.xpath('//table[@id="accountTransactionsTable"]/tbody/tr/td[1]/a/text()')]
        table = zip(
            date,
            [self.name]*len(date),
            [g.replace(',','.') for g in v.xpath('//table[@id="accountTransactionsTable"]/tbody/tr/td[4]/span/text()')],
            v.xpath('//table[@id="accountTransactionsTable"]/tbody/tr/td[3]/text()')
        )[::-1]
        
        return left, table