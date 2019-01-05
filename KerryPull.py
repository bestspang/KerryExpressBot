from bs4 import BeautifulSoup as soup
from html.parser import HTMLParser
from urllib.request import urlopen as uReq
import json, requests, random, os
import numpy as np
import pandas as pd

track_id = 'SMLP000341000'

def getTable(track_id):
    if track_id == 0:
        return 0
    #SAMPLE :: https://th.kerryexpress.com/th/track/?track=SMLP000341000 # SEA's SAMPLE
    print("\n")
    url = 'https://th.kerryexpress.com/th/track/?track=' + track_id
    print("connecting.. : " + url + "\n")

    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',})
    site_request = requests.get(url, headers=headers)
    site_content = soup(site_request.content, "html.parser") #lxml
    #uClient = uReq(url)
    #page_html = uClient.read()
    #uClient.close()
    #page_soup = soup(page_html, "html.parser")
    #return(site_content)
    return site_content.findAll("div", {"class":"col"})#("table", {"class":"table table-info"})

def stockPrice(track_id):
    if track_id == 0 or track_id == None:
        return 0
    price = getTable(track_id)
    try:
        price = price[2].text.strip()
        text = ('หุ้น {} ราคาปัจจุบันอยู่ที่ {} บาท'.format(track_id, price))
        return (text, price)
    except:
        return ('ไม่มีข้อมูลหุ้นตัวนี้', None)

def main():
    print(getTable(track_id))

if __name__ == "__main__":
    main()
