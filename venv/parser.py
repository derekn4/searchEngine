import os, json
import re
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import math


sno = nltk.stem.SnowballStemmer('english')

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
def get_tokens(content, words):
    tokens = []
    for t in content.text.split():
        tokens = re.split(r'[^a-z0-9]+', t.lower())
        words.extend(tokens)

    for word in words:
        if len(word) >= 2 and not word.isdigit():
            if word != '':
                tokens += [word]
    return tokens

def count_freq_url(tokens):
    word_dict1 = dict()
    for word in tokens:
        if word not in stop_words:
            if word not in word_dict1.keys():
                if word != '':
                    word_dict1[word] = 1
                    if word in doc_freq.keys():
                        # print(word, " : ", sno.stem(word))
                        doc_freq[word] += 1
                        if sno.stem(word) in doc_freq.keys():
                            doc_freq[sno.stem(word)] += 1
                        else:
                            doc_freq[sno.stem(word)] = 1
                    else:
                        # print(word, " : ", sno.stem(word))
                        doc_freq[word] = 1
                        doc_freq[sno.stem(word)] = 1
            else:
                if word != '':
                    word_dict1[word] += 1
                    if word in doc_freq.keys():
                        doc_freq[word] += 1
                        if sno.stem(word) in doc_freq.keys():
                            doc_freq[sno.stem(word)] += 1
                        else:
                            doc_freq[sno.stem(word)] = 1
                    else:
                        doc_freq[word] = 1
                        doc_freq[sno.stem(word)] = 1
    return word_dict1

class ParserScript():
    def ParseCorpus(self):
        token_list = []
        doc_urls = dict()
        doc_freq = dict()
        count = 0
        doc_space = []
        final_list = []
        corpus_size = len([f for root, dirs, files in os.walk("DEV") for f in files if f.endswith('.json')])
        for root, dirs, files in os.walk("DEV"):
            for f in files:
                if f.endswith(".json"):
                    count+=1
                    data = json.load(open(os.path.join(root,f)))
                    items = dict(data.items())
                    doc_urls["doc"+str(count)] = items["url"]
                    content = BeautifulSoup(items["content"],"lxml")
                    tokenized_text = get_tokens(content, token_list)

                    for tk in tokenized_text:
                        if tk not in doc_space and tk!="":
                            doc_space.append(tk)

                    token_dict = count_freq_url(tokenized_text)

                    for k,v in token_dict.items():
                        text = k+' doc'+ str(count) + ":"+str(v)
                        final_list.append(text)

        with open("Store/docspace.txt", "w") as f:
            f.write(str(doc_space))
        with open("Store/docfrequencies.txt", "w") as g:
            g.write(str(doc_freq))
        with open("Store/docurls.txt", "w") as h:
            h.write(str(doc_urls))

        tup = (corpus_size, len(doc_space), final_list, doc_space, doc_freq)
        return tup