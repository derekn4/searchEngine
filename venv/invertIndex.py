from collections import defaultdict
import math
from nltk import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer


#use nltk to stem works

ps = PorterStemmer()
class invertIndexer():
    def __init__(self):
        self.__dict = defaultdict(list)
        self.__docMags = {}

    def BuildIndex(self):
        count = 0
        for direct in os.listdir("DEV"):
            for i in os.listdir("DEV\\" + direct):
                if i.endswith(".json"):
                    count += 1