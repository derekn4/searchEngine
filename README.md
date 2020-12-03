1. Upload DEV folder into same directory as invertIndex.py

2. Run the invertIndex.py program

3. Wait for “Store” folder to populate with partial indexes, docIDs, and docFrequencies

4. Wait for tf-idf calculation and mergeIndex

5. Program will prompt user for a query after finished

6. Type “quit” to end search engine

7. If re-run after finishing corpus and calculating tf-idf, comment out lines
      #282 ParseCorpus(corpusPaths)
      #285 calculatetfidf(docfreq, len(corpusPaths)
