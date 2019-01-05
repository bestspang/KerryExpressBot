from pythainlp.tokenize import word_tokenize, isthai
from bs4 import BeautifulSoup as soup
from html.parser import HTMLParser
from urllib.request import urlopen as uReq

def extractWord(text):
    a = word_tokenize(text, engine='newmm')
    b = []
    for h in a:
        if h != ' ':
            b.append(h)
    return b

def checkth(lists):
    for i in range(len(lists)):
        if isthai(lists[i])['thai'] == 0:
            return lists[i]
    return 0

def stockPrice(stock_quote):
    if stock_quote == 0:
        return 0
    stock_quote = stock_quote.upper()
    url = 'https://www.settrade.com/C04_01_stock_quote_p1.jsp?txtSymbol='+ stock_quote +'&ssoPageId=9&selectPage=1'
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    price = page_soup.findAll("div", {"class":"col-xs-6"})
    try:
        price = price[2].text.strip()
        return ('หุ้น {} ราคาปัจจุบันอยู่ที่ {} บาท'.format(stock_quote, price))
    except:
        return ('ไม่มีข้อมูลหุ้นตัวนี้')



text = input('thai sentence: ')
words_list = extractWord(text)
print(words_list)
if 'หุ้น' in words_list or 'ราคา' in words_list:
    print(stockPrice(checkth(words_list)))
