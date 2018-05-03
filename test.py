
import unicodedata
from mtranslate import translate
import os
import json
import sys, getopt
#import fitz
#import pdfquery
import re

from bs4 import BeautifulSoup

translatedFileName = "translated1.txt"
JSONFilename = "outputJSON1.txt"
translatedFile = open(translatedFileName, "w")
jsonFile = open(JSONFilename, "w")

def translator(text):
    try:
        text = translate(text,'en', 'es')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

id = 0
mydct = {}
lst = []
with open('kmeans_clusters1.txt') as f:
    for line in f:
        id = id + 1
        splitline = line.split("\t")
        cluster = splitline[0]
        data = splitline[1]
        headlinesplit = splitline[1].split("<<<>>>")
        headline = headlinesplit[0]
        news = headlinesplit[1]
        innerdct = {}
        innerdct['id'] = id
        innerdct['headline'] = headline
        innerdct['news'] = news
        if cluster in mydct:
            mydct[cluster].append(innerdct)
        else:
            lst = []
            lst.append(innerdct)
            mydct[cluster] = lst
        news = news[:100]
        try:
            translateheadline = translator(headline)
            translatenews = translator(news)
        except:
            pass
        writestr = str(cluster)+"\t"+translateheadline+"\t"+translatenews+"\n"
        print(writestr)
        translatedFile.write(writestr)

jsonWrite = json.dumps(mydct, sort_keys=True,indent=4, separators=(',', ': '))
jsonFile.write(jsonWrite)