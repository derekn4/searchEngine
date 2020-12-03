Upload DEV folder into same directory as invertIndex.py

Run the invertIndex.py program

Wait for “Store” folder to populate with partial indexes, docIDs, and docFrequencies

Wait for tf-idf calculation and mergeIndex

Program will prompt user for a query after finished

Type “quit” to end search engine

If re-run after finishing corpus and calculating tf-idf, comment out lines
#282 ParseCorpus(corpusPaths)
#285 calculatetfidf(docfreq, len(corpusPaths)
