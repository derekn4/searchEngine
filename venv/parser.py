import os, json
import re
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize, sent_tokenize

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

word_dict = dict()
docID_dict = dict()

url_tokens = dict()

docID_lists = []
#def parse(corpusPath):
#    corpus_size = len([direct for direct in os.listdir(corpusPath) if direct.endswith(".txt")])


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
            tokens += [word]

    return tokens

def count_freq(tokens):
    word_dict1 = dict()
    for word in tokens:
        if word not in stop_words:
            if word not in word_dict1.keys():
                word_dict1[word] = 1
            else:
                word_dict1[word] += 1
    return word_dict1

token_list = []
count = 0


for direct in os.listdir("DEV"):
    for i in os.listdir("DEV\\" + direct):
        if i.endswith(".json"):
            count += 1  # increment corpus Size
            file = "DEV\\" + direct + "\\" + i  # get file Path
            data = json.load(open(file))        # json.load file makes dict of file data
            docID_dict[count] = data["url"]
            content = BeautifulSoup(data['content'], "lxml")
            tokenized_text = get_tokens(content, token_list)
            token_dict = count_freq(tokenized_text)
            for token in token_dict:
                url_tokens[token] = [[count], token_dict[token]]
            if count==200:
                break
    if count==200:
        break

sort_dict = {k: v for k, v in sorted(word_dict.items(), key=lambda item: item[1], reverse=True)}
print(url_tokens)
print(docID_dict)
print(sort_dict)
