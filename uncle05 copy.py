from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from html.parser import HTMLParser
import numpy as np
import pandas as pd

#stock_quote = stock_quote.upper()
#url = 'http://www.settrade.com/C13_MarketSummary.jsp?detail=SET50'
#url = 'https://www.settrade.com/C04_01_stock_quote_p1.jsp?txtSymbol='+ stock_quote +'&ssoPageId=9&selectPage=1'
url = 'http://www.settrade.com/C13_MarketSummary.jsp?order=Y&market=SET'
uClient = uReq(url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
#price = page_soup.findAll("div", {"class":"col-xs-6"})
##price = page_soup.findAll("div", {"class":"col-xs-12 col-md-8"})
#price = page_soup.findAll("table", {"class":"table table-info"})
price = page_soup.findAll("div", {"class":"col-sm-6 col-xs-12"})
# for i in range(len(price)):
#     print(price[i].text.strip().replace(' ', ''))

def makeDF(soupdata, ind=0):
    row_list = []
    head_list = []
    tr_list = soupdata[ind].findAll('tr')
    for tr in tr_list:
            th_list = tr.findAll('th')
            if th_list is not None:
                for th in th_list:
                    head_list.append(th.text.replace(' ', '').strip().split('\r')[0])
            td_list = tr.findAll('td')

            for td in td_list:
                row_list = np.append(row_list, td.text.replace(' ', '').strip())
    head_list[0] = 'SYMBOL'
    num_col = len(head_list)
    total_col = int(len(row_list)/num_col)
    row_list = np.reshape(row_list, (total_col, num_col) )
    return pd.DataFrame(columns = head_list, data = row_list)

print(makeDF(price))

#print(head_list)
# for i in range(len(price[0])):
#     print(price[0].contents[i])

#price = price[0].text.strip().replace(' ', '')
#print(price.splitlines())

#price = price[2].text.strip()
