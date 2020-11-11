import os, json
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize

def parse(corpusPath):
    corpus_size = len([direct for direct in os.listdir(corpusPath) if direct.endswith(".txt")])
