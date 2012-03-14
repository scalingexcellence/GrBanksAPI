#!/usr/bin/python
# -*- coding: utf-8 -*-

from basebank import BaseBank

import lxml,time
from BeautifulSoup import UnicodeDammit

class Alpha(BaseBank):
    def __init__(self, user=None, passw=None, acnt=None, name="ALPHA"):
        super(Alpha, self).__init__(name)
        if user!=None: self.load(user,passw,acnt)
            
    def _load(self, user, passw=None, acnt=None):
        (user,passw,acnt)=self.manage_up(user,passw,acnt)
    
        (s,v)=self.openUrl('https://secure.alpha.gr/e-services/')

        action = v.xpath("//form//input")

        params = dict([(g.attrib['name'], g.attrib['value']) for g in action if 'name' in g.attrib and 'value' in g.attrib])

        params['ctl00$_contentPlaceHolder$_loadedControl_NewLayoutSignOn$_userName'] = user
        params['ctl00$_contentPlaceHolder$_loadedControl_NewLayoutSignOn$_Pswd'] = passw
        t='ctl00$_contentPlaceHolder$_loadedControl_NewLayoutSignOn$_login'
        params[t]=params[t].encode('utf-8')

        #Login
        (s,v)=self.openUrl('https://secure.alpha.gr/e-services/Login.aspx?service=NewLayoutSignOn', params)

        #Get list of accounts/statements
        (s,v)=self.openUrl('https://secure.alpha.gr/e-services/AWBPage.aspx?service=balancesStatements')

        action = v.xpath("//form//input[@name='__VIEWSTATE']/@value")

        params = [
            ('__LASTFOCUS',''),
            ('__EVENTTARGET','ctl00$_contentPlaceHolder$_loadedControl_balancesStatements$_statementsButton'),
            ('__EVENTARGUMENT',''),
            ('__VIEWSTATE', action[0]),
            ('__VIEWSTATEENCRYPTED',''),
            ('ctl00$_mainMenu',''),
            ('ctl00$_contentPlaceHolder$_loadedControl_balancesStatements$_productsPagedDropDownList$_selectedIndexHiddenField','1'),
            ('ctl00$_contentPlaceHolder$_loadedControl_balancesStatements$_productsPagedDropDownList$_selectedOrderIndexHiddenField','-1'),
            ('ctl00$_contentPlaceHolder$_loadedControl_balancesStatements$_productsPagedDropDownList$_selectionList',acnt),
            ('ctl00$_faxNumberPanel$_faxNumber$_textValue','')
        ]

        #Get balance for the account
        (s,v)=self.openUrl('https://secure.alpha.gr/e-services/AWBPage.aspx?service=balancesStatements', params)

        def decode_html(html_string):
            converted = UnicodeDammit(html_string, isHTML=True)
            if not converted.unicode:
                raise UnicodeDecodeError("Failed to detect encoding, tried [%s]", ', '.join(converted.triedEncodings))
            return converted.unicode
        def nophone(adr):
            g = adr.find(u' Τηλέφωνα')
            return adr if g==-1 else adr[0:g]
            
        v=lxml.html.fromstring(decode_html(s))
    
        #Extract transactions info
        rep = [
            {
                'date': r.xpath("td[1]/text()")[0].strip(),
                'desc': "%s | %s" % (r.xpath("td[2]/*/text()")[0].strip(), nophone(r.xpath("td[3]/span/@title")[0].replace('\r\n',' '))),
                'amount': "%s%s" % ('-' if r.xpath("td[5]/text()")[0].strip()==u'Χ' else '', r.xpath("td[4]/text()")[0].strip().replace(',','.')),
                'total': "%s%s" % ('-' if r.xpath("td[7]/text()")[0].strip()==u'Χ' else '', r.xpath("td[6]/text()")[0].strip().replace(',','.'))
            }
            for r in v.xpath("//table[@class='ResultTable']//tr[@bgcolor]")]
        
        #Pack transactions to the table
        left = rep[len(rep)-1]['total']
        table = zip(
            map(lambda s:time.strptime(s['date'],'%d/%m/%Y'), rep),
            [self.name]*len(rep),
            map(lambda s:s['amount'], rep),
            map(lambda s:s['desc'], rep)
        )
        return left, table