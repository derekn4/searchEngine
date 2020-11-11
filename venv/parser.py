import os, json
import re
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize, sent_tokenize


#def parse(corpusPath):
#    corpus_size = len([direct for direct in os.listdir(corpusPath) if direct.endswith(".txt")])


#Count size of Corpus
#Make dictiornary of number: json file
def get_tokens(content, words):
    tokens = []
    for t in content.text.split():
        tokens = re.split(r'[^a-z0-9]+', t.lower())
        words.extend(tokens)

    for word in words:
        if len(word) >= 2 and not word.isdigit():
            tokens += [word]

    return tokens

token_list = []
count = 0
for direct in os.listdir("DEV"):
    for i in os.listdir("DEV\\" + direct):
        if i.endswith(".json"):
            count+=1                            #increment corpus Size
            file = "DEV\\" + direct + "\\" + i  #get file Path
            data = json.load(open(file))        #json.load file makes dict of file data
            print(data['content'])
            content = BeautifulSoup(data['content'], "lxml")
            print(content)
            tokenized_text = get_tokens(content, token_list)
            print(tokenized_text)
        break
    break

print(count)
