import os, json
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import math
from nltk import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import nltk
from itertools import chain
import glob
import ast

'''
Derek Nguyen - 44096504
Alex Meng - 12907102
'''

# Count size of Corpus
# Make dictiornary of number: json file
# Make list of Token : [[docIDs where found], tf-dif]
sno = nltk.stem.SnowballStemmer('english')

invert_dict = dict()
doc_freq = dict()
storage_index_file = []
index_file_count = 0
index_list = []

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
        if word not in word_dict1.keys():
            if word != '':
                #word_dict1[word] = 1
                word_dict1[sno.stem(word)] = 1
        else:
            if word != '':
                # word_dict1[word] += 1
                if sno.stem(word) in word_dict1.keys() and sno.stem(word) != word:
                    word_dict1[sno.stem(word)] += 1
                else:
                    word_dict1[sno.stem(word)] = 1

        if word in doc_freq.keys():
            #doc_freq[word] += 1
            if sno.stem(word) in doc_freq.keys() and sno.stem(word) != word:
                doc_freq[sno.stem(word)] += 1
            else:
                doc_freq[sno.stem(word)] = 1
        else:
            #doc_freq[word] = 1
            doc_freq[sno.stem(word)] = 1

    return word_dict1

def mergeIndex(temp, index):
    temp_index = open(temp, "r")
    temp2 = open("Store/temp_index2.txt", "a+")
    temp2.truncate(0)
    index_file = open(index, "w")
    temp_list = []
    temp2_list = []
    count = 0
    merge = defaultdict(list)

    for t in temp_index:
        res = ast.literal_eval(t)
        temp_list.append(res)
    # print(len(temp_list))

    merge = temp_list[0]
    while count < len(temp_list):
        count += 1
        for k, v in chain(merge.items(), temp_list[count].items()):
            if k not in merge.keys():
                merge[k] = v
            else:
                merge[k].extend(v)
        if count % 15 == 0:
            temp2.write(str(merge) + "\n")
            merge = dict()
        if count == len(temp_list) - 1:
            temp2.write(str(merge) + "\n")
            merge = dict()

    for t in temp2:
        res = ast.literal_eval(t)
        temp2_list.append(res)

    # merge = dict(merge)
    # index_file.write(str(merge) + "\n")
    # index_file.close()
    temp_index.close()


def BuildIndex(tks, file, corpusSize, docID, count):
    global index_file_count
    global index_list

    temp_index = open(file, 'a')

    global invert_dict
    for t, frq in tks.items():
        if t not in invert_dict:
            invert_dict[t] = [docID + ":" + str(frq)]
        else:
            invert_dict[t].append(docID + ":" + str(frq))

    if count % 10000 == 0:
        index_list.extend(file)
        temp_index.write(str(invert_dict) + "\n")
        temp_index.close()
        invert_dict = dict()

        index_file_count += 1

    elif count == corpusSize:
        index_list.extend(file)
        temp_index.write(str(invert_dict) + "\n")
        temp_index.close()
        invert_dict = dict()

        index_file_count += 1


def ParseCorpus(jsonFiles):
    doc_urls = dict()
    count = 0
    corpus_size = len(jsonFiles)
    global index_file_count

    # try...except
    for f in jsonFiles:
        try:
            count += 1
            data = json.load(open(f))
            items = dict(data.items())
            doc_urls["doc" + str(count)] = items["url"]

            content = BeautifulSoup(items["content"], "lxml")
            tokenized_text = get_tokens(content)

            token_dict = count_freq_url(tokenized_text)

            sort_dict = {k: v for k, v in sorted(token_dict.items(), key=lambda item: item[0], reverse=True)}
            BuildIndex(sort_dict, 'Store/index' + str(index_file_count) + '.txt', corpus_size, "doc" + str(count), count)

            if count % 100 == 0:
                print(count)
        except:
            continue
    with open("Store/docfrequencies.txt", "w") as g:
        g.write(str(doc_freq))
    with open("Store/docurls.txt", "w") as h:
        h.write(str(doc_urls))


tempindexfile = "Store/temp_index.txt"
indexfile = "Store/index.txt"

corpusPaths = glob.glob("DEV\*\*.json")
ParseCorpus(corpusPaths)

# mergeIndex(tempindexfile, indexfile)

# open the temp_index.txt
# turn str into dict
# merge with defaultdict + chain
