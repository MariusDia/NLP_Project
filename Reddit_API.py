# -*- coding: utf-8 -*-

import time

from class_architecture import PreProcessSubmissionCollection, SentenceProcessSubmissionCollection, SubmissionCollection

from wordcount import calculateJacquard, pearsonCorrelation

from histograms import separateOverlapSubCommentHists
from histograms import mixedOverlapSubCommentHists

def main():
    # nltk.download('stopwords')
    # nltk.download('punkt')
    # nltk.download('wordnet')
    #Main loop, parameters input (query, subReddit, submission limit, comment limit)

    #Main loop, parameters input (query, subReddit, submission limit, comment limit)
    print("Climate Change News Analysis. Discovering Arguments")
    continueBool = input("Do you want to start a new search ? (y,n): ")
        
    #Continuing the loop
    #while(True)
    if continueBool=='y':
        query = input("Enter a query : ")
        subReddit = input("What subreddit do you want to browse (type 'all' for browsing everything): ")
        subLimit = int(input("How much submissions do you want to process: "))
        comLimit = int(input("How much comments per submissions do you want to process: "))
        print("Processing request... \n")
        
        start_time = time.time()
        subColl = SubmissionCollection(subLimit,comLimit, query, subReddit)
        #subCollPreProcess = PreProcessSubmissionCollection(subColl)
        #subCollSentenceProcess = SentenceProcessSubmissionCollection(subColl)
        subCollPreProcess = PreProcessSubmissionCollection(subLimit,comLimit, query, subReddit)
        subCollSentenceProcess = SentenceProcessSubmissionCollection(subLimit,comLimit, query, subReddit)
        print("Execution time for " + str(subLimit) + " submissions, with " + str(comLimit) + " comments each : " + str((time.time() - start_time)) + " seconds\n")
        
        print("List of averge comment's length per submission : " + str(subCollPreProcess.getCommentLengthAverage()) + "\n")
        
        #Subloop, what to display (histogram mixed/seperate histogram)
        #while(True):
        print("Now, what to display ?\n")
        mode = input("Histogram (type 'hist'), Jaccard indexes (type 'jacc'), Pearson correlation (type 'pears') others?, or to stop the display loop, type 'stop'")
        if mode == "hist":
            sepMix = input("Seperate or Mixed Word Overlap (s/m)")
                
            if sepMix=="s":
                print("Drawing (comments words are separeted) articles/comments histograms ...\n")
                separateOverlapSubCommentHists(subCollPreProcess)
            elif sepMix=="m":
                print("Drawing (comments words are mixed) articles/comments histograms ...\n")
                mixedOverlapSubCommentHists(subCollPreProcess)
                time.sleep(1.0)
                
        elif mode=="jacc":
            print("Jaccard index :\n")
            print(calculateJacquard(subCollPreProcess))

        elif mode=="pears":
            print("Pearson correlation :\n")
            print(pearsonCorrelation(subCollSentenceProcess))

        elif mode=="stop":
            pass
            #break
            
    #Stoping the looping
    elif continueBool=='n':
        print("Goodbye !")
        #break

    #Wrong input
    else :
        print("Wrong input, please retry !")

subColl = main()
