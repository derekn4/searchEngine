import os, json
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import math
from nltk import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import nltk
import glob

#from parser import ParserScript

#use nltk to stem works
stop_words = ['about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren",
              'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
              "can", 'cannot', 'could', "couldn", 'did', "didn", 'do', 'does', "doesn", 'doing', "don",
              'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn", 'has', "hasn", 'have',
              "haven't", 'having', 'he', 'her', 'here', 'hers', 'herself', 'him',
              'himself', 'his', 'how', "how's", 'if', 'in', 'into', 'is',
              "isn", 'it', 'its', 'itself', 'me', 'more', 'most', "mustn", 'my', 'myself',
              'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our',
              'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she',
              'should', "shouldn", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs',
              'them', 'themselves', 'then', 'there', 'these', 'they',
              'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn",
              'we', 'were', "weren", 'what', 'when',
              'where', 'which', 'while', 'who', 'whom', 'why', 'with', "won",
              'would', "wouldn", 'you', "ll", "re", "ve", 'your', 'yours', 'yourself',
              'yourselves']


#Count size of Corpus
#Make dictiornary of number: json file
#Make list of Token : [[docIDs where found], tf-dif]
sno = nltk.stem.SnowballStemmer('english')

invert_dict = dict()

def get_tokens(content):
    tokens = []
    words = []
    for t in content.text.split():
        tokens = re.split(r'[^a-z0-9]+', t.lower())
        words.extend(tokens)

    for word in words:
        if len(word) >= 2 and not word.isdigit():
                tokens += [word]
    return tokens

def count_freq_url(tokens):
    word_dict1 = dict()
    for word in tokens:
        if word not in stop_words:
            if word not in word_dict1.keys():
                if word != '':
                    word_dict1[word] = 1
                    # if word in doc_freq.keys():
                    #     doc_freq[word] += 1
                    #     if sno.stem(word) in doc_freq.keys():
                    #         doc_freq[sno.stem(word)] += 1
                    #     else:
                    #         doc_freq[sno.stem(word)] = 1
                    # else:
                    #     doc_freq[word] = 1
                    #     doc_freq[sno.stem(word)] = 1
            else:
                if word != '':
                    word_dict1[word] += 1
                    # if word in doc_freq.keys():
                    #     doc_freq[word] += 1
                    #     if sno.stem(word) in doc_freq.keys() and sno.stem(word) != word:
                    #         doc_freq[sno.stem(word)] += 1
                    #     else:
                    #         doc_freq[sno.stem(word)] = 1
                    # else:
                    #     doc_freq[word] = 1
                    #     doc_freq[sno.stem(word)] = 1
    return word_dict1

def BuildIndex(tks, file, corpusSize, docID, count):
    index = open(file, 'w')
    global invert_dict
    for t,frq in tks.items():
        if t not in invert_dict:
            invert_dict[t] = [docID + ":" + str(frq)]
        else:
            invert_dict[t].append(docID+":"+str(frq))

    if count%1000==0:
        index.truncate(0)
        index.write(str(invert_dict) + "\n")
        index.close()
        #invert_dict = dict()

def ParseCorpus(jsonFiles):
    doc_urls = dict()
    count = 0
    #token_count = 0
    #final_list = []
    corpus_size = len(jsonFiles)
    for f in jsonFiles:
        count += 1
        data = json.load(open(f))
        items = dict(data.items())
        doc_urls["doc" + str(count)] = items["url"]

        content = BeautifulSoup(items["content"], "lxml")
        tokenized_text = get_tokens(content)

        # for tk in tokenized_text:
        #     if tk not in doc_space and tk != "":
        #         token_count+=1
        token_dict = count_freq_url(tokenized_text)
        #token : file_freq

        # sort dict alphabetically
        sort_dict = {k: v for k, v in sorted(token_dict.items(), key=lambda item: item[0], reverse=True)}
        # build index after tokenizing
        BuildIndex(sort_dict, "Store/index.txt", corpus_size, "doc"+str(count), count)

        # for k, v in token_dict.items():
        #     text = k + ' doc' + str(count) + ":" + str(v)
        #     final_list.append(text)
        if count%100==0:
            print(count)
        if count==20000:
            break
    # with open("Store/docspace.txt", "w") as f:
    #     f.write(str(doc_space))
    # with open("Store/docfrequencies.txt", "w") as g:
    #     g.write(str(doc_freq))
    with open("Store/docurls.txt", "w") as h:
        h.write(str(doc_urls))

    #tup = (corpus_size, len(doc_space), final_list, doc_freq)
    #return tup


# ps = PorterStemmer()
# class invertIndexer():
#     def __init__(self):
#         self.__dict = defaultdict(list)
#         self.__docMags = {}
#
#     def BuildIndex(self, tks, file, corpusSize, docfreq):
#         index = open(file, 'w')
#         n = 0                           #basically docID
#         for t in tks:
#             #Token + ' doc' + str(count) + ":" + doc_freq
#             t = t.split()               #[token, doc1:freq]
#             t2 = t[1].split(":")        #[doc1, freq]
#             self.tfidf = docfreq[t[0]]  #t2[1]
#
#             self.__dict[t[0]].append(t2[0]+":"+str(self.tfidf)) #inverted Index
#                                         #{token : [doc1:freq, doc2:freq2]}
#         index.write(str(dict(self.__dict)))
#         index.close()

indexfile = "Store/index.txt"

corpusPaths = glob.glob("DEV\*\*.json")
ParseCorpus(corpusPaths)
#tup = ParseCorpus(corpusPaths)
#indexer = invertIndexer()

#indexer.BuildIndex(tup[2], indexfile, tup[0], tup[3])
