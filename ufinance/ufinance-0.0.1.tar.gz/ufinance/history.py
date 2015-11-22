# -*- coding: utf8 -*-

import urllib2
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from pandas.io.common import urlencode
import re

def google(code="KOSDAQ%3A016170", ei="w3lRVoiLM9Cc0QSa1J6gCA",
           start=datetime.datetime.today()-datetime.timedelta(days=7), end=datetime.datetime.today(),
           urlview=1):
    # URL
    _GOOGLE_URL = "https://www.google.com/finance/historical?q="+code+"&"
    url = "%s%s" % (_GOOGLE_URL,
                    urlencode({"startdate": start.strftime('%b %d, ' '%Y'),
                               "enddate": end.strftime('%b %d, %Y'),
                               "ei": ei
                              }))
    if urlview:
        print url

    # Data Read
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'lxml')
    a = soup.find(id='prices')
    # Data Parsing
    label = []
    for i in a.findAll("th"):
        label.append(i.text.replace('\n',''))
    value = []
    for i in a.findAll("td", { "class" : re.compile("^(rgt|lm)$") }):
        value.append(i.text.replace('\n',''))

    # Spliting
    valueData = []
    length = len(label)
    temp = []
    for idx, v in enumerate(value):
        if v[0].isdigit():
            v = v.replace(',','')
            v = float(v)
        if idx%length == 0 and idx>0:
            valueData.append(temp)
            temp = []
        temp.append(v)
    valueData.append(temp)

    # Pandas
    df = pd.DataFrame(valueData, columns=label)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date').sort()

    return df