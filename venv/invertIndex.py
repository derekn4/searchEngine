from collections import defaultdict
import math

class invertIndexer():
    def __init__(self):
        self.__dict = defaultdict(list)
        self.__docMags = {}