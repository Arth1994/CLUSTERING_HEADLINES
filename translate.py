
import unicodedata
from mtranslate import translate
import os
import json
import sys, getopt
#import fitz
#import pdfquery
import re

from bs4 import BeautifulSoup

translatedFileName = "translated.txt"
JSONFilename = "outputJSON.txt"
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
tmydct = {}
lst = []
tlst = []
with open('kmeans_clusters.txt') as f:
    for line in f:
        id = id + 1
        splitline = line.split("\t")
        cluster = splitline[0]
        data = splitline[1]
        headlinesplit = splitline[1].split("<<<>>>")
        headline = headlinesplit[0]
        news = headlinesplit[1]
        innerdct = {}
        transdct = {}
        innerdct['news'] = news
        innerdct['id'] = id
        innerdct['cluster'] = cluster
        innerdct['headline'] = headline
        transdct['id'] = id
        transdct['cluster'] = cluster
        news = news[:200]
        try:
            translateheadline = translator(headline)
            translatenews = translator(news)
            transdct['headline'] = translateheadline
            transdct['news'] = translatenews
        except:
            pass
        if cluster in mydct:
            mydct[cluster].append(innerdct)
            tmydct[cluster].append(transdct)
        else:
            lst = []
            tlst = []
            lst.append(innerdct)
            tlst.append(transdct)
            mydct[cluster] = lst
            tmydct[cluster] = tlst
            #translatedFile.write(writestr)

jsonWrite = json.dumps(mydct, sort_keys=True,indent=4, separators=(',', ': '))
jsonFile.write(jsonWrite)

tWrite = json.dumps(tmydct, sort_keys=True,indent=4, separators=(',', ': '))
translatedFile.write(tWrite)
print(tWrite)