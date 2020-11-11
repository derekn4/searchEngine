from collections import defaultdict
import math
from nltk import word_tokenizesent_tokenize
from nltk.stem import PorterStemmer


#use nltk to stem works

ps = PorterStemmer()
class invertIndexer():
    def __init__(self):
        self.__dict = defaultdict(list)
        self.__docMags = {}