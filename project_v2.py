#from cStringIO import StringIO
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage

import unicodedata
from mtranslate import translate
import os
import json
import sys, getopt
#import fitz
import pdfquery
import re

from bs4 import BeautifulSoup

textFilename = "tup.txt"
cleanedFilename = "cleanup.txt"
jsonfilename = "to_kmeans.txt"

#os.system("pdf2txt.py -o C:\\Users\\devan\\Downloads\\UTD\\2018 Spring\\Big Data\\Project\\spanishTest.html -t html C:\\Users\\devan\\Downloads\\UTD\\2018 Spring\\Big Data\\Project\\spanishTest.pdf")

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text).lower()



sizeCutoff = 39
textFile = open(textFilename, "w") #make text file
cleanedFile = open(cleanedFilename, "w")
jsonFile = open(jsonfilename, "w")

htmlData = open("ElHorizonte.html", 'r')
soup = BeautifulSoup(htmlData, "html.parser")

font_spans = [ data for data in soup.select('span') if 'font-size' in str(data) ]
output = []

fonts_size_prev = 0
count = 0
strNews = ""
currHeadline = ""
mydct = {}
    
for i in font_spans:
    fonts_size = re.search(r'(?is)(font-size:)(.*?)(px)',str(i.get('style'))).group(2)
    txt = str(u''.join(i.text).encode('utf-8').strip())
    txt = strip_accents(txt)
    
    if (abs(fonts_size_prev - int(fonts_size)) > 0) and int(fonts_size) > sizeCutoff and len(txt)>2 and len(txt.split(" ")) > 1:
        if currHeadline != "":
            jsonFile.write("\n")
            jsonFile.write(currHeadline + "<<<>>>" + strNews)
        currHeadline = ""
        strNews = ""
        cleanedtxt = " ".join(re.findall("[a-zA-Z]+", txt))
        currHeadline += cleanedtxt + " "
        if fonts_size_prev != 0:
            textFile.write("\n")
            cleanedFile.write("\n")
            jsonFile.write("\n")
        #textFile.write(fonts_size)
        #cleanedFile.write(fonts_size)
        #textFile.write("\t")
        #cleanedFile.write("\t")
        textFile.write(txt)
        cleanedFile.write(cleanedtxt)
        fonts_size_prev = int(fonts_size)
           
    elif int(fonts_size) > sizeCutoff and len(txt)>2 and abs(fonts_size_prev - int(fonts_size)) ==  0 and len(txt.split(" ")) > 1:
        cleanedtxt = " ".join(re.findall("[a-zA-Z]+", txt))
        currHeadline += cleanedtxt
        textFile.write(" ")
        cleanedFile.write(" ")
        textFile.write(txt)
        cleanedFile.write(cleanedtxt)
    
    elif int(fonts_size) < 15:
        cleanedtxt = " ".join(re.findall("[a-zA-Z]+", txt))
        strNews += cleanedtxt + " "
            
