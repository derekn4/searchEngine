import os, json
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenizesent_tokenize
from nltk.stem import PorterStemmer

#def parse(corpusPath):
#    corpus_size = len([direct for direct in os.listdir(corpusPath) if direct.endswith(".txt")])
#hey there
#use nltk to stem works

ps = PorterStemmer()

print(os.listdir("DEV"))
count = 0
for direct in os.listdir("DEV"):
    for i in os.listdir("DEV\\" + direct):
        if i.endswith(".json"):
            count+=1

print(count)