import os
import csv
from pythainlp.tokenize import word_tokenize
#import itertools

class Prepare(object):
    #def __init__(self):
    #self.fileInput = fileInput
    def extractWord(self, alist):
        a = word_tokenize(alist, engine='newmm')
        b = []
        for h in a:
            if h != ' ':
                b.append(h)
        return b

    def rands(self, a):
        if a == 0:
            return("Received")
        elif a == 1:
            return("Sent")

    def delAll(self, a):
        open(a, 'w').close()

def run():
    p = Prepare()
    text = input('thai sentence: ')
    print(p.extractWord(alist = text))

if __name__ == '__main__':
    run()
