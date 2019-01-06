from bs4 import BeautifulSoup as soup
from html.parser import HTMLParser
from urllib.request import urlopen as uReq
import requests, argparse
import numpy as np
import pandas as pd

Parser = argparse.ArgumentParser(prog= "Parser")
Parser.description= "This will return the shipping status by adding TrackID"
Parser.add_argument("-track_id", help= "please add your tracking ID", required=True)
args = Parser.parse_args()

col_vars = ['due', 'receiver', 'sender', 'status', 'name', 'datetime', 'city']

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
    site_content = soup(site_request.content, "html.parser") #lxml
    site_data = site_content.findAll("div", {"class":"col colStatus"}) #("table", {"class":"table table-info"})
    return site_data

def cleanData(site_data, ind=0):
    list = []
    lay1 = ['status piority-success', 'status normaly-waiting']
    lay2 = ['date', 'd1', 'd2']
    for i in range(len(lay1)):
        status = site_data[0].findAll("div", {"class":lay1[i]})
        if status is not None:
            for j in range(len(status)):
                print("\n ================= \n ")
                for k in range(len(lay2)):
                    data = status[j].findAll("div", {"class":lay2[k]})
                    if k == 0:
                        data = data[0].findAll("div")
                        data = [data[m].text.replace(' ', '').strip() for m in range(2)]
                        data = [''.join(data[n].split('e')[1:3]) for n in range(2)]
                    elif k == 1 and i == 0:
                        data = data[0].text.replace(' ', '').strip()
                        data = [data.split('(')[0],data. split('(')[1].split(')')[0], data.split('\n')[2]]
                    elif k == 1 and i != 0:
                        data = data[0].text.replace(' ', '').strip()
                        data = [data, None, None]
                    else:
                        data = data[0].text.replace(' ', '').strip()
                        data = [data]
                    print(str(data) + "\n ------------------")
                    list.append(data)
    print("\n ================= \n ")
    return list

def list_flatten(l, a=None):
    if a is None:
        a = []
    for i in l:
        if isinstance(i, list):
            list_flatten(i, a)
        else:
            a.append(i)
    return a

def makeDF(outlist):
    head_list = ['date', 'time', 'status', 'receiver', 'name', 'city']
    num = int(len(outlist) / 6)
    a = np.array(outlist)
    a = a.reshape((num, 6))
    return pd.DataFrame(columns = head_list, data = a), a

def main():
    #track_id = 'SMLP000341000'
    track_id = args.track_id
    print(args)
    #track_id = input("Type your Track-ID: ")
    data = getData(track_id)
    clean_data = cleanData(data)
    flat_data = list_flatten(clean_data)
    df, b = makeDF(flat_data)

    new = df["city"].str.split("-", n = 1, expand = True)
    df["city"] = new[0]
    df["country"] = new[1]
    c = df.to_json(orient='index', force_ascii=False)
    return(c)

if __name__ == "__main__":
    main()
