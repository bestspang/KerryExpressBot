from bs4 import BeautifulSoup as soup
from html.parser import HTMLParser
from urllib.request import urlopen as uReq
import json, requests, random, os
import numpy as np
import pandas as pd

track_id = 'SMLP000341000'
col_vars = ['due', 'receiver', 'sender', 'status', 'name', 'datetime', 'city']
col_names = ['due', 'receiver', 'sender', 'status', 'name', 'datetime', 'city']

def getData(track_id):
    if track_id == 0:
        return 0
    #SAMPLE :: https://th.kerryexpress.com/th/track/?track=SMLP000341000 # SEA's SAMPLE
    print("\n")
    url = 'https://th.kerryexpress.com/th/track/?track=' + track_id
    print("connecting.. : " + url + "\n")

    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',})
    site_request = requests.get(url, headers=headers)
    site_content = soup(site_request.content, "html.parser")
    site_data = site_content.findAll("div", {"class":"col colStatus"})
    return site_data

#def makeDF(site_data, ind=0):
#    d2_list = site_data[ind].findAll('d2')
#    return d2_list
    #for tr in d2_list:
    #    print(tr + "================= \n")
        #th_list = tr.findAll('th')
        #head_list.append(th.text.replace(' ', '').strip().split('\r')[0])

siteText = getData(track_id)
lay1 = ['status piority-success', 'status normaly-waiting']
lay2 = ['date', 'd1', 'd2']

for i in range(len(lay1)):
    status = siteText[0].findAll("div", {"class":lay1[i]})
    if status is not None:
        for j in status:
            print("\n =================")
            for k in range(len(lay2)):
                data = j.findAll("div", {"class":lay2[k]})
                data = data[0].text.replace(' ', '').strip()
                #data = data.text.replace(' ', '').strip().split('\r')
                print("\n" + str(data) + "\n ------------------")

#print(tr)
#print(htmlText)
