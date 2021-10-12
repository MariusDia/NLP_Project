# -*- coding: utf-8 -*-
import praw

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

import requests
from bs4 import BeautifulSoup

from praw.models import MoreComments

import time

import numpy as np
import matplotlib.pyplot as plt



#Reddit API authentification
reddit = praw.Reddit(
    client_id="9aC2iDzQQi04w-q1cPmjUw",
    client_secret="O29M5Puueuew1y_rDYVuvUZLdKuF_w",
    user_agent="NLP_Project_API/0.0.1",
)


#Text processing (tokenization, stop words removal)
def preProcess(doc):
    Stopwords = list(set(nltk.corpus.stopwords.words('english')))
    stemmer = SnowballStemmer("english")
    WN_lemmatizer = WordNetLemmatizer()

    sentences = sent_tokenize(doc)
    Tokens = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [stemmer.stem(word) for word in words]
        words = [WN_lemmatizer.lemmatize(word, pos="v") for word in words]
        
        words = [word for word in words if word.isalpha() and word not in Stopwords] #get rid of numbers and Stopwords
        Tokens.extend(words)
        
    return ' '.join(Tokens)


#-----------Class architecture---------------

class Comment:
    def __init__(self, pComment):
        self.body = pComment.body


class Article:
    def __init__(self, url):
        self.url = url
        
        res = requests.get(url)
        soup = BeautifulSoup(res.text)
        self.content = preProcess(soup.get_text().strip())


#Simplified version of praw Submission class model
class Submission:
    
    
    def __init__(self, pSubmission, comLimit):
        self.title = pSubmission.title
        self.article = Article(pSubmission.url)
        #self.author = pSubmission.author
        #self.popularity = pSubmission.score  #number of upvotes
        
        self.comments = []
        #setting Submissions comments
        i=0
        for comment in pSubmission.comments:
            if not(isinstance(comment, MoreComments)) and ('I am a bot' not in comment.body):
                self.comments.append(Comment(comment))
                i+=1
            if i>=comLimit:
                break
            
            
class SubmissionCollection:
    def __init__(self, subLimit, comLimit, query, subReddit):
        self.subLimit=subLimit
        self.query=query
        self.subReddit=subReddit
        
        self.submissions=[]
        #setting submissions in the collection
        i=0
        for submission in reddit.subreddit(subReddit).search(query):
            self.submissions.append(Submission(submission, comLimit))
            i+=1
            if i>=subLimit:
                break
            
        #Text processing (tokenization and stopword removal)
        #Submission title processing
        for sub in self.submissions:
            sub.title = preProcess(sub.title)
            #Comments content processing
            for comment in sub.comments:
                comment.body = preProcess(comment.body)
        
    def getCommentLengthAverage(self):
        comLengthList = []
        for sub in self.submissions:
            comLengthSum = 0
            for com in sub.comments:
                comLengthSum += len(com.body)
            
            if len(sub.comments)==0:
                comLengthList.append(-1)
            else:
                comLengthList.append(comLengthSum/len(sub.comments))
        return comLengthList
    
#-------------Main class, for testing----------------------

def main():
    print("Climate Change News Analysis. Discovering Arguments")
    query = input("Enter a query : ")
    subReddit = input("What subreddit do you want to browse (type 'all' for browsing everything): ")
    subLimit = int(input("How much submissions do you want to process: "))
    comLimit = int(input("How much comments per submissions do you want to process: "))
    print("Processing request... \n")
    
    start_time = time.time()
    subColl = SubmissionCollection(subLimit,comLimit, query, subReddit)
    print("\nExecution time for " + str(subLimit) + " submissions, with " + str(comLimit) + " comments each : " + str((time.time() - start_time)) + " seconds")
    print("List of averge comment's length : " + str(subColl.getCommentLengthAverage()))
    print("\n")
    
    return subColl

subColl = main()


#----------------Word counting-----------------

def getSubWordCounting(subColl, subNum, wordLimit=10):
    '''

    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.
    subNum : int
        index of the Submission in subColl.
    wordLimit : int, optional
        Number limit of words (the 'wordLimit' most common word) . The default is 10.

    Returns a dictionary of the "wordLimit" most common words in a submission article 
    -------
    subWordCount : dict
        A dictionary of the "wordLimit" most common words in a submission article.

    '''
    subWordCount = {}
    
    #Getting word counting
    sub = subColl.submissions[subNum]
    
    for word in sub.article.content.split():
        if word not in subWordCount.keys():
            subWordCount[word] = 1
        else:
            subWordCount[word] += 1
    
    
    #Sorting and taking only 10 most common words
    subWordCount = {k: v for k, v in sorted(subWordCount.items(), key=lambda item: item[1], reverse=True)}
    for i in range(len(subWordCount)-wordLimit):
        subWordCount.popitem()
            
    return subWordCount


def getCommentWordCounting(subColl, subNum, comNum, wordLimit=10):
    '''

    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.
    subNum : int
        index of the Submission in subColl.
    comNum : int
        index of the comment in the Submission comments list.
    wordLimit : int, optional
        Number limit of words (the 'wordLimit' most common word) . The default is 10.

    Returns a dictionary of the "wordLimit" most common words in a comment 
    -------
    subCommentCount : dict
        A dictionary of the "wordLimit" most common words in a comment.

    '''
    subCommentCount = {}
    
    #Getting word counting
    for word in subColl.submissions[subNum].comments[comNum].body.split():
        if word not in subCommentCount.keys():
            subCommentCount[word] = 1
        else:
            subCommentCount[word] += 1
    
            
    #Sorting and taking only 100 most common words of the first comment
    subCommentCount =  {k: v for k, v in sorted(subCommentCount.items(), key=lambda item: item[1], reverse=True)}
    for i in range(len(subCommentCount)-wordLimit):
        subCommentCount.popitem()
    return subCommentCount


#List of word counting dictionaries for every comments of first submission
def getSubCommentsWordCounting(subColl, subNum, wordLimit=10):
    '''

    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.
    subNum : int
        index of the Submission in subColl.
    wordLimit : int, optional
        Number limit of words (the 'wordLimit' most common word) . The default is 10.

    Returns a list of 
    -------
    comWordCountList : list 
        List of dictionaries of the "wordLimit" most common words of every chosen comments of a submission.

    '''
    
    comWordCountList =[]
    sub = subColl.submissions[subNum]
    for i in range(len(sub.comments)):
        comWordCountList.append(getCommentWordCounting(subColl,subNum, i, wordLimit))
    return comWordCountList

def getMergedComWordCount(subColl, subNum, wordLimit=20):
    '''
    

    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.
    subNum : int
        index of the Submission in subColl.
    wordLimit : int, optional
        Number limit of words (the 'wordLimit' most common word) . The default is 20.

    Returns
    -------
    mergedComWordCount : TYPE
        DESCRIPTION.

    '''
    mergedComWordCount = {}
    for sub in subColl.submissions:
        for com in sub.comments:
            for word in com.body.split():
                if word not in mergedComWordCount.keys():
                    mergedComWordCount[word] = 1
                else:
                    mergedComWordCount[word] += 1
    #Sorting and taking only 100 most common words of the first comment
    mergedComWordCount =  {k: v for k, v in sorted(mergedComWordCount.items(), key=lambda item: item[1], reverse=True)}
    for i in range(len(mergedComWordCount)-wordLimit):
        mergedComWordCount.popitem()
    
    return mergedComWordCount

#mergedComWordCount = getMergedComWordCount(subColl, 0)
#print(mergedComWordCount)

#-------------------Histograms of word counting----------------



#Histogram drawing of Word Overlapping for a sub and its comments separated

def separateSubCommentsHist(subWordCount, comWordCountList):
    '''

    Parameters
    ----------
    subWordCount : dict
        A dictionary of the "wordLimit" most common words in a submission article.
    comWordCountList : list
        List of dictionaries of the "wordLimit" most common words of every chosen comments of a submission.

    Draws an histogram of word overlapping of ONE SUBMISSION and EACH of its COMMENTS
    -------
    None.

    '''
    #♣Figure initialization
    #Sublopts count = comments count
    fig, axs = plt.subplots(len(comWordCountList))
    fig.suptitle('Stacked subplots, submission counting/comment counting')
    i=0
    #Sub plots input
    for comCount in comWordCountList:
        print(str(i) + "  " + str(len(comWordCountList)))
        axs[i].bar(list(subWordCount.keys()), subWordCount.values(), color='b')
        axs[i].bar(list(comCount.keys()), comCount.values(), color='g')
        i+=1
        
        
def separateOverlapSubCommentHists(subColl, subWordLimit, comWordLimit):
    '''

    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.
    subWordLimit : int
        Select the 'subWordLimit' most common words of SUBMISSION.
    comWordLimit : int
        Select the 'comWordLimit' most common words of COMMENTs.

    Draws X histograms of word overlapping of EVERY SUBMISSION and EACH of their COMMENTS
    -------
    None.

    '''
    for subNum in range(len(subColl.submissions)):
        comWordCountList = getSubCommentsWordCounting(subColl, subNum, comWordLimit)
        if len(comWordCountList)<5:
            print("not much comments on this post : " + subColl.submissions[subNum].title)
        if len(comWordCountList)>1:
            subWordCount = getSubWordCounting(subColl, subNum, subWordLimit)
            separateSubCommentsHist(subWordCount,comWordCountList)
        else:
            print("No comments ? " + str(subColl.submissions[subNum].title))




#Histogram drawing of Word Overlapping for a sub and its comments separated7

subWordLimit=10
comWordLimit=10
def mixedOverlapSubCommentHists(subColl, subWordLimit=10, comWordLimit=10):
    '''

    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.
    subWordLimit : int, optional
        Select the 'subWordLimit' most common words of SUBMISSION. The default is 10
    comWordLimit : int, optional
        Select the 'comWordLimit' most common words of COMMENTs. The default is 10

    Draws X histograms of word overlapping of EVERY SUBMISSION and EVERY one of their COMMENTS
    -------
    None.

    '''
    for i in range(len(subColl.submissions)):
        mergedComWordCount = getMergedComWordCount(subColl, i, subWordLimit)
        subWordCounting = getSubWordCounting(subColl, i, comWordLimit)
        
        fig, axs = plt.subplots()
        
        axs.bar(list(subWordCounting.keys()), subWordCounting.values(), color='g', label='Article Word Counting')
        axs.bar(list(mergedComWordCount.keys()), mergedComWordCount.values(), color='b', label='Comments Word Counting')


'''subWordCount =  getSubWordCounting(subColl, 0)
print("Word Counting of submission's article content")
print(subWordCount)
print("\n")

comNum=0
subCommentCount = getCommentWordCounting(subColl,0 , comNum)
print("Word Counting of submission's " + str(comNum+1) + "th comment")
print(subCommentCount)
print("\n")'''

'''wordLimit=10
comWordCountList = getSubCommentsWordCounting(subColl, 0, wordLimit)

subWordLimit=10
comWordLimit=10
print("Drawing (separate comments) articles/comments histograms ...\n")
separateOverlapSubCommentHists(subColl, subWordLimit, comWordLimit)'''

print("Drawing (separate comments) articles/comments histograms ...\n")
mixedOverlapSubCommentHists(subColl)


    
