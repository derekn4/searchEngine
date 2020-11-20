import os, json
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import math
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
final_query_list = []
final_freq_list = []
storage_index_file = []
index_file_count = 0
index_list = []
#index_list = ["Store\\index0.txt","Store\\index1.txt","Store\\index2.txt","Store\\index3.txt","Store\\index4.txt","Store\\index5.txt"]
merge = defaultdict(list)

def get_tokens(content):
    tokens = []
    words = []
    for t in content.split():
        tokens = re.split(r'[^a-z0-9]+', t.lower())
        words.extend(tokens)
    for word in words:
         if len(word) >= 2 and not word.isdigit():
             tokens += [word]
    return tokens

def count_freq_url(tokens, size_doc):
    word_dict1 = dict()
    for word in tokens:
        if sno.stem(word) not in word_dict1.keys():
            if word != '':
                word_dict1[sno.stem(word)] = 1
        else:
            if word != '':
                word_dict1[sno.stem(word)] += 1

        if sno.stem(word) in doc_freq.keys():
            if word!="":
                doc_freq[sno.stem(word)] += 1
        else:
            if word!="":
                doc_freq[sno.stem(word)] = 1

    #CALCULATING TF (for tf-idf)
    for k,v in word_dict1.items():
        #tf = count of t in doc / num of tks in doc
        word_dict1[k] = round((v/size_doc), 2) #--> what if 0?

    return word_dict1


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

def calculatetfidf(index_list, docfreq, corpusSize):
    corp_freq = open(docfreq, "r")

    for t in corp_freq:
        freqs = ast.literal_eval(t)

    for database in index_list:
        file = open(database, "a+")
        count = 0

        for t in file:
            tk_docs = ast.literal_eval(t)

        for k,v in tk_docs.items():
            for docs in range(len(v)):
                dfreq = v[docs].split(":")
                d = dfreq[0]
                freq = int(dfreq[1])
                tfidf = round(((1 + math.log(freq)) * math.log((corpusSize/(freqs[k]+1)))),2)
                v[docs] = d + ":" + str(abs(tfidf))

        file.truncate(0)
        file.write(str(tk_docs))
        file.close()



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
            tokenized_text = get_tokens(content.text.lower())
            size_doc = len(tokenized_text)
            token_dict = count_freq_url(tokenized_text, size_doc)

            sort_dict = {k: v for k, v in sorted(token_dict.items(), key=lambda item: item[0].lower())}
            BuildIndex(sort_dict, 'Store/index' + str(index_file_count) + '.txt', corpus_size, "doc" + str(count), count)

            if count % 100 == 0:
                print(count)
        except:
            continue

    with open("Store/docfrequencies.txt", "w") as g:
        g.write(str(doc_freq))
    with open("Store/docurls.txt", "w") as h:
        h.write(str(doc_urls))

def mergeIndex(index_list):
    global merge
    count = 0

    while count<len(index_list):
        curr_index = open(index_list[count], "r")
        count+=1
        next_index = open(index_list[count], "r")
        for t in curr_index:
            res1 = ast.literal_eval(t)

        for t in next_index:
            res2 = ast.literal_eval(t)

        for k, v in chain(res1.items(), res2.items()):
            if k not in merge.keys():
                merge[k] = v
            else:
                merge[k].extend(v)
        count+=1


def queryDatabase():
    global merge
    while True:
        query = input("Search the index(type quit to exit): ")

        if query=="quit":
            exit()

        search = [sno.stem(word) for word in query.split()]

        query_dict = dict()
        final_dict = dict()
        query_list = []
        freq_list = []

        if search[0] in merge.keys():
            for t in merge[search[0]]:
                dfreq = t.split(":")
                dtk = dfreq[0]
                freq = dfreq[1]
                query_list.append(dtk)
                freq_list.append(int(freq))

        if len(search) > 1:
            for i in range(1, len(search)):
                temp = []
                temp_freq_list = []
                count = 0
                if search[i] in merge.keys():
                    for t in merge[search[i]]:
                        dfreq = t.split(":")
                        dtk = dfreq[0]
                        temp_freq = dfreq[1]
                        temp.append(dtk)
                        temp_freq_list.append(int(temp_freq))

                while count < len(query_list):
                    if query_list[count] not in temp:
                        query_list.pop(count)
                        freq_list.pop(count)
                    else:
                        freq_list[count] += temp_freq_list[temp.index(query_list[count])]
                        count += 1


        for i in range(len(query_list)):
            final_dict[query_list[i]] = freq_list[i]

        sort_dict = {k: v for k, v in sorted(final_dict.items(), key=lambda item: item[1], reverse=True)}
        url_file = open("Store\\docurls.txt", "r")
        for t in url_file:
            urls = ast.literal_eval(t)

        sort_count = 0
        final_docs = []
        for k,v in sort_dict.items():
            if sort_count==5:
                break
            final_docs.append(urls[k])
            sort_count+=1

        print("Results for ", query, ": \n")
        for i in range(len(final_docs)):
            print(str(i+1) + " : " + final_docs[i])

            
#might just get rid of docfreq variable b/c global variable doc_freq
docfreq = "Store\\docfrequencies.txt"
corpusPaths = glob.glob("DEV\*\*.json")

#1: parse files and builds partial inverted indexes {token: "docId:tf
ParseCorpus(corpusPaths)

#2: goes through the partial inverted indexes and calculates tf-idf scores
calculatetfidf(index_list, docfreq, len(corpusPaths))

#3: merges the partial indexes into 1 global index variable
mergeIndex(index_list)

#4: query Database (REQUIRED: search is <1 second aka ~300ms)
queryDatabase()

