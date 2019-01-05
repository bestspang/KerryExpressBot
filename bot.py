from flask import Flask, request, abort
import json, requests, random, os
import dialogflow
import numpy as np
import pandas as pd
from pythainlp.tokenize import word_tokenize, isthai
from bs4 import BeautifulSoup as soup
from html.parser import HTMLParser
from urllib.request import urlopen as uReq
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

app = Flask(__name__)

line_bot_api = LineBotApi('Z7FgW5zgSO1G9BaHiMJOCKTByoH6Fl9gFIam59JdkfVXaavM8k8DEsEfLZpWmBlNDbWv/q4wYA0mY/gJWLfNUBFX8yNp+5A5THgSjLzx6DTLVi5x69Ejbd1JRLBOtiS7/HoOmKHJDvmmlDEt2DXj1QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1b8e881368efe90738ce5c3341898c35')

@app.route("/")
def hello():
    return "This is BP_LINEBOT2!"

@app.route("/bot", methods=['POST'])
def bot():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def extractWord(text):
    a = word_tokenize(text, engine='newmm')
    b = []
    for h in a:
        if h != ' ':
            b.append(h)
    return b

def getSymbol(lists):
    for i in range(len(lists)):
        if isthai(lists[i])['thai'] == 0:
            return lists[i].upper()
    return 0

def getTable(stock_quote):
    if stock_quote == 0:
        return 0
    #url = 'http://www.settrade.com/C13_MarketSummary.jsp?detail=SET50'
    url = 'https://www.settrade.com/C04_01_stock_quote_p1.jsp?txtSymbol='+ stock_quote +'&ssoPageId=9&selectPage=1'
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup.findAll("div", {"class":"col-xs-6"})#("table", {"class":"table table-info"})

def stockPrice(stock_quote):
    if stock_quote == 0 or stock_quote == None:
        return 0
    price = getTable(stock_quote)
    try:
        price = price[2].text.strip()
        text = ('หุ้น {} ราคาปัจจุบันอยู่ที่ {} บาท'.format(stock_quote, price))
        return (text, price)
    except:
        return ('ไม่มีข้อมูลหุ้นตัวนี้', None)

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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    words_list = extractWord(event.message.text)
    if 'หุ้น' in words_list or 'ราคา' in words_list:
        symbo = getSymbol(words_list)
        price, money = stockPrice(symbo)
        if symbo == 'SET' or symbo == 'SET50':
            price = 'กำลังอัพเดทระบบ SET ค่ะหนูน้อย ใจเย็นๆ'
        elif price == 0:
            return 0
        else:
            if not is_number(money):
                price = 'ราคายังไม่มีการอัพเดทครัช'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=price))
        return 0

    if event.message.text.lower().replace(' ','') == 'Most Active Value'.lower().replace(' ',''):
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text='Most Active Value'))
        return 0
    if event.message.text.lower().replace(' ','') == 'Most Active Volume'.lower().replace(' ',''):
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text='Most Active Volume'))
        return 0
    if event.message.text.lower().replace(' ','') == 'Top Gainers'.lower().replace(' ',''):
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text='Top Gainers'))
        return 0
    if event.message.text.lower().replace(' ','') == 'Top Losers'.lower().replace(' ',''):
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text='Top Losers'))
        return 0

    ce = random.randint(1,10)
    if ce > 6 and ce < 9:
        text = ['ตูดหมึก', 'หอย', 'WTF!', 'ขี้โม้', 'ไม่เชื่อ!', 'แม่ย้อย', 'พ่อง', 'โฮ่งง', 'สลัดผัก']
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text[random.randint(0,8)]))

if __name__ == "__main__":
    app.run()
