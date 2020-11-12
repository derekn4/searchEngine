import os, json
import re
from bs4 import BeautifulSoup
import nltk
import collections
from nltk import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import math
import glob

#nltk.download('punkt')
doc_freq = dict()
doc_urls = dict()
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
corpusPaths = glob.glob("DEV\*\*.json")
sno = nltk.stem.SnowballStemmer('english')
indexfile = "Store/index.txt"

def initInvertedIndex():
    index = open(indexfile, 'w')
    invIndex = dict()
    count = 0
    for doc in corpusPaths:
        count+=1
        data = json.load(open(doc))
        items = dict(data.items())
        doc_urls["doc" + str(count)] = items["url"]
        with open(doc) as file:
            soup = BeautifulSoup(file, "lxml")
            tokenizer = nltk.RegexpTokenizer(r'\w+')
            findTokens(invIndex, soup, tokenizer, doc, count)

        if count<1000 and count%100==0:
            print(count)
        elif count>1000 and count%50==0:
            #print(invIndex)
            print(count)
        if count==2000:
            break

    for term, path_frq in invIndex.items():
        doc_freq[term] = path_frq
    index.write(str(doc_freq))
    index.close()

    with open("Store/docfrequencies.txt", "w") as g:
        g.write(str(invIndex))
    with open("Store/docurls.txt", "w") as h:
        h.write(str(doc_urls))


def findTokens(invIndex, soup, tokenizer, document, count):
    tokens = []
    for content in soup.find_all("body"):
        for term in tokenizer.tokenize(content.text):
            term = re.sub('[^A-Za-z]', '', term)
            if len(term)>1:
                tokens.append(term.lower())
        counts = collections.Counter(tokens)
        for term, frq in counts.items():
            if term not in invIndex:
                invIndex[term] = ""
            termFrq = float(frq)
            obj = "doc"+str(count) + " : " + str(termFrq) + " "
            invIndex[term] += obj

    #print(invIndex)

# def get_tokens(content, words):
#     tokens = []
#     for t in content.text.split():
#         tokens = re.split(r'[^a-z0-9]+', t.lower())
#         words.extend(tokens)
#
#     for word in words:
#         if len(word) >= 2 and not word.isdigit():
#             if word != '':
#                 tokens += [word]
#     return tokens
#
# def count_freq_url(tokens):
#     word_dict1 = dict()
#     for word in tokens:
#         if word not in stop_words:
#             if word not in word_dict1.keys():
#                 if word != '':
#                     word_dict1[word] = 1
#                     if word in doc_freq.keys():
#                         # print(word, " : ", sno.stem(word))
#                         doc_freq[word] += 1
#                         if sno.stem(word) in doc_freq.keys():
#                             doc_freq[sno.stem(word)] += 1
#                         else:
#                             doc_freq[sno.stem(word)] = 1
#                     else:
#                         # print(word, " : ", sno.stem(word))
#                         doc_freq[word] = 1
#                         doc_freq[sno.stem(word)] = 1
#             else:
#                 if word != '':
#                     word_dict1[word] += 1
#                     if word in doc_freq.keys():
#                         doc_freq[word] += 1
#                         if sno.stem(word) in doc_freq.keys():
#                             doc_freq[sno.stem(word)] += 1
#                         else:
#                             doc_freq[sno.stem(word)] = 1
#                     else:
#                         doc_freq[word] = 1
#                         doc_freq[sno.stem(word)] = 1
#     return word_dict1
#
# class ParserScript():
#     def ParseCorpus(self):
#         token_list = []
#         doc_urls = dict()
#         doc_freq = dict()
#         count = 0
#         doc_space = []
#         final_list = []
#         corpus_size = len([f for root, dirs, files in os.walk("DEV") for f in files if f.endswith('.json')])
#         for root, dirs, files in os.walk("DEV"):
#             for f in files:
#                 if f.endswith(".json"):
#                     count+=1
#                     data = json.load(open(os.path.join(root,f)))
#                     items = dict(data.items())
#                     doc_urls["doc"+str(count)] = items["url"]
#                     content = BeautifulSoup(items["content"],"lxml")
#                     tokenized_text = get_tokens(content, token_list)
#
#                     for tk in tokenized_text:
#                         if tk not in doc_space and tk!="":
#                             doc_space.append(tk)
#
#                     token_dict = count_freq_url(tokenized_text)
#
#                     for k,v in token_dict.items():
#                         text = k+' doc'+ str(count) + ":"+str(v)
#                         final_list.append(text)
#
#         with open("Store/docspace.txt", "w") as f:
#             f.write(str(doc_space))
#         with open("Store/docfrequencies.txt", "w") as g:
#             g.write(str(doc_freq))
#         with open("Store/docurls.txt", "w") as h:
#             h.write(str(doc_urls))
#
#         tup = (corpus_size, len(doc_space), final_list, doc_space, doc_freq)
#         return tup

if __name__=="__main__":
    initInvertedIndex()
    print(doc_freq)

