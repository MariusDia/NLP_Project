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

#Most common words sorting (first submission title)
def getSubWordCounting2(subColl, subNum, wordLimit):
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

subWordCount =  getSubWordCounting2(subColl, 0, 10)
print("Word Counting of submission's article content")
print(subWordCount)
print("\n")


#Most common words sorting (submission comment)
def getCommentWordCounting(subColl, subNum, comNum, wordLimit):
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

comNum=0
subCommentCount = getCommentWordCounting(subColl,0 , comNum, 10)
print("Word Counting of submission's " + str(comNum+1) + "th comment")
print(subCommentCount)
print("\n")


#List of word counting dictionaries for every comments of first submission
def getSubCommentsWordCounting(subColl, subNum, wordLimit):
    comWordCountList =[]
    sub = subColl.submissions[subNum]
    for i in range(len(sub.comments)):
        comWordCountList.append(getCommentWordCounting(subColl,subNum, i, wordLimit))
    return comWordCountList

wordLimit=5
comWordCountList = getSubCommentsWordCounting(subColl, 0, wordLimit)
for l in comWordCountList:
    print(l)
print("\n")

#-------------------Histograms of word counting----------------

#Histogram drawing of one sub and its comments 
def subCommentsHisto(subWordCount, comWordCountList):
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
        
        
        
print("Drawing articles/comments histograms ...\n")
#subCommentsHisto(subWordCount,comWordCountList)

subWordLimit=10
comWordLimit=10
for subNum in range(len(subColl.submissions)):
    comWordCountList = getSubCommentsWordCounting(subColl, subNum, comWordLimit)
    if len(comWordCountList)<5:
        print("not much comments on this post : " + subColl.submissions[subNum].title)
    if len(comWordCountList)>1:
        subWordCount = getSubWordCounting2(subColl, subNum, subWordLimit)
        subCommentsHisto(subWordCount,comWordCountList)
    else:
        print("No comments ? " + str(subColl.submissions[subNum].title))
    
    
