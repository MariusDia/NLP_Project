# -*- coding: utf-8 -*-

import time

from class_architecture import SubmissionCollection

from wordcount import calculateJacquard
from wordcount import pearsonCorrelation

from histograms import separateOverlapSubCommentHists
from histograms import mixedOverlapSubCommentHists
from negative_sent import negative_entities
from LDA import performLDA


def main():
    # nltk.download('stopwords')
    # nltk.download('punkt')
    # nltk.download('wordnet')
    # Main loop, parameters input (query, subReddit, submission limit, comment limit)

    # Main loop, parameters input (query, subReddit, submission limit, comment limit)
    print("Climate Change News Analysis. Discovering Arguments")
    
    try:
        continueBool = input("Do you want to start a new search ? (y,n): ")
    
        # Continuing the loop
        # while(True)
        if continueBool == 'y':
            query = input("Enter a query : ")
            subReddit = input("What subreddit do you want to browse (type 'all' for browsing everything): ")
            subLimit = int(input("How much submissions do you want to process: "))
            comLimit = int(input("How much comments per submissions do you want to process: "))
            print("Processing request... \n")
    
            start_time = time.time()
            subColl = SubmissionCollection(subLimit, comLimit, query, subReddit)
            print("Execution time for " + str(subLimit) + " submissions, with " + str(comLimit) + " comments each : " + str(
                (time.time() - start_time)) + " seconds\n")
    
            print("List of averge comment's length per submission : " + str(subColl.getCommentLengthAverage()) + "\n")
    
            # Subloop, what to display (histogram mixed/seperate histogram)
            # while(True):
            print("Now, what to display ?\n")
            mode = input(
                "Histogram (type 'hist'), Jaccard indexes (type 'jacc'), others?, or to stop the display loop, type 'stop'")
            if mode == "hist":
                sepMix = input("Seperate or Mixed Word Overlap (s/m)")
    
                if sepMix == "s":
                    print("Drawing (comments words are separeted) articles/comments histograms ...\n")
                    separateOverlapSubCommentHists(subColl)
                elif sepMix == "m":
                    print("Drawing (comments words are mixed) articles/comments histograms ...\n")
                    mixedOverlapSubCommentHists(subColl)
                    time.sleep(1.0)
    
            #Jacquard
            elif mode == "jacc":
                print("Jaccard index :\n")
                print(calculateJacquard(subColl))
                
            #LDA model
            elif mode == 'lda':
                print(performLDA(subColl, 3))
                
            #Pearson
            elif mode=="pears":
                print("Pearson correlation :\n")
                print(pearsonCorrelation(subColl))
                
            elif mode == "stop":
                pass
                # break
    
        # Stoping the looping
        elif continueBool == 'n':
            print("Goodbye !")
            # break
    except:
        print("Unknown error")

    # Wrong input
    else:
        print("Wrong input, please retry !")


# main()




subLimit=3
comLimit=20
query="industrial farming"
subReddit="news"
print("Processing submission collection... \n\n")
subColl = SubmissionCollection(subLimit, comLimit, query, subReddit)
negative_entities(subColl)
"""

print('pearson')
print(pearsonCorrelation(subColl))
#print("Drawing separate histogram")
#separateOverlapSubCommentHists(subColl)
#print("Drawing mixed histogram\n\n")
#mixedOverlapSubCommentHists(subColl)

'''print("Jaccard index :\n\n")
print(calculateJacquard(subColl))

print("LDA model\n\n")
print(performLDA(subColl, 3))

print("Pearson\n\n")
print(pearsonCorrelation(subColl))'''
"""