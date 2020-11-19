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
final_query_list = []
final_freq_list = []
storage_index_file = []
index_file_count = 0
index_list = []

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

def count_freq_url(tokens):
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
    return word_dict1

# def mergeIndex(temp, index):
#     temp_index = open(temp, "r")
#     temp2 = open("Store/temp_index2.txt", "a+")
#     temp2.truncate(0)
#     index_file = open(index, "w")
#     temp_list = []
#     temp2_list = []
#     count = 0
#     merge = defaultdict(list)
#
#     for t in temp_index:
#         res = ast.literal_eval(t)
#         temp_list.append(res)
#     # print(len(temp_list))
#
#     merge = temp_list[0]
#     while count < len(temp_list):
#         count += 1
#         for k, v in chain(merge.items(), temp_list[count].items()):
#             if k not in merge.keys():
#                 merge[k] = v
#             else:
#                 merge[k].extend(v)
#         if count % 15 == 0:
#             temp2.write(str(merge) + "\n")
#             merge = dict()
#         if count == len(temp_list) - 1:
#             temp2.write(str(merge) + "\n")
#             merge = dict()
#
#     for t in temp2:
#         res = ast.literal_eval(t)
#         temp2_list.append(res)
#
#     # merge = dict(merge)
#     # index_file.write(str(merge) + "\n")
#     # index_file.close()
#     temp_index.close()


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
        file = open(database, "r")
        count = 0

        for t in file:
            tk_docs = ast.literal_eval(t)


        for k,v in tk_docs.items():
            if count==10:
                break
            for docs in range(len(v)):
                dfreq = v[docs].split(":")
                d = dfreq[0]
                freq = int(dfreq[1])
                #print(k + "=" + str(freqs[k]))
                tfidf = round(((1 + math.log(freq))*math.log((corpusSize/freqs[k]))), 2)
                v[docs] = d + ":" + str(abs(tfidf))
            count+=1
        break

    print(tk_docs["6pm"])
    print(tk_docs["7pm"])
    print(tk_docs["about"])
    print(tk_docs["all"])
    # for k,v in tk_docs.items():
    #     print("key:", k, " val:",v)



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

            token_dict = count_freq_url(tokenized_text)

            sort_dict = {k: v for k, v in sorted(token_dict.items(), key=lambda item: item[0].lower())}
            BuildIndex(sort_dict, 'Store/index' + str(index_file_count) + '.txt', corpus_size, "doc" + str(count), count)

            if count % 100 == 0:
                print(count)
        except:
            continue
    with open("Store/docfrequencies2.txt", "w") as g:
        g.write(str(doc_freq))
    with open("Store/docurls2.txt", "w") as h:
        h.write(str(doc_urls))

def queryDatabase(index_list):
    query = input("Search the index(type quit to exit): ")

    if query=="quit":
        exit()

    search = [sno.stem(word) for word in query.split()]

    print(search)

    query_dict = dict()
    final_dict = dict()
    query_list = []
    freq_list = []
    for database in index_list:
        file = open(database, "r")
        for t in file:
            res = ast.literal_eval(t)

        if search[0] in res.keys():
            for t in res[search[0]]:
                dfreq = t.split(":")
                dtk = dfreq[0]
                freq = dfreq[1]
                query_list.append(dtk)
                freq_list.append(int(freq))

            #token                  #["docID:freq", ...]
            query_dict[search[0]] = res[search[0]]
        if len(search)>1:
            for i in range(1,len(search)):
                score = []
                temp = []
                temp_freq_list = []
                count = 0
                if search[i] in res.keys():
                    for t in res[search[i]]:
                        dfreq = t.split(":")
                        dtk = dfreq[0]
                        temp_freq = dfreq[1]
                        #lopes docs
                        temp.append(dtk)

                        #lopes freq
                        temp_freq_list.append(int(temp_freq))

                while count<len(query_list):
                    if query_list[count] not in temp:
                        query_list.pop(count)
                        freq_list.pop(count)
                    else:
                        freq_list[count] += temp_freq_list[temp.index(query_list[count])]
                        count+=1
        #print("final query_list3")
        final_query_list.extend(query_list)
        final_freq_list.extend(freq_list)
        if len(final_query_list)==len(final_freq_list):
            print("Searching...")
        file.close()

    for i in range(len(final_query_list)):
        final_dict[final_query_list[i]] = final_freq_list[i]

    sort_dict = {k: v for k, v in sorted(final_dict.items(), key=lambda item: item[1], reverse=True)}

    url_file = open("Store\\docurls2.txt", "r")
    for t in url_file:
        urls = ast.literal_eval(t)

    sort_count = 0
    final_docs = []
    for k,v in sort_dict.items():
        if sort_count==5:
            break
        final_docs.append(urls[k])
        sort_count+=1

    print()
    for i in range(len(final_docs)):
        print(str(i+1) + " : " + final_docs[i])




tempindexfile = "Store\\temp_index.txt"
indexfile = "Store\\index.txt"

docfreq = "Store\\docfrequencies2.txt"
corpusPaths = glob.glob("DEV\*\*.json")
# ParseCorpus(corpusPaths)

#calculatetfidf(index_list, docfreq, len(corpusPaths))

# mergeIndex(tempindexfile, indexfile)
queryDatabase(index_list)

