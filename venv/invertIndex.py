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
        #make dictionary "index"
        n = 0 #basically docID

        #for all documents do
        for direct in os.listdir("DEV"):
            for i in os.listdir("DEV\\" + direct):
                if i.endswith(".json"):
                    n += 1
                    #T (tokenize) parse i json file
                    #remove duplicates from T
                    #for all tokens in T do:
                        #if token not in index.keys()
                            #Posting = posting_list
                            #index[t] = [posting]
                        #index[t].append(posting(n))
        #return index