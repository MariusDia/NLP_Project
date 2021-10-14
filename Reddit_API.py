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

from wordcount import *
from histograms import *

import numpy as np
import matplotlib.pyplot as plt

# Reddit API authentification
reddit = praw.Reddit(
    client_id="9aC2iDzQQi04w-q1cPmjUw",
    client_secret="O29M5Puueuew1y_rDYVuvUZLdKuF_w",
    user_agent="NLP_Project_API/0.0.1",
)


# Text processing (tokenization, stop words removal)
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

        words = [word for word in words if word.isalpha() and word not in Stopwords]  # get rid of numbers and Stopwords
        Tokens.extend(words)

    return ' '.join(Tokens)


# -----------Class architecture---------------

class Comment:
    def __init__(self, pComment):
        self.body = pComment.body


class Article:
    def __init__(self, url):
        self.url = url

        res = requests.get(url)
        soup = BeautifulSoup(res.text)
        self.content = preProcess(soup.get_text().strip())


# Simplified version of praw Submission class model
class Submission:

    def __init__(self, pSubmission, comLimit):
        self.title = pSubmission.title
        self.article = Article(pSubmission.url)
        # self.author = pSubmission.author
        # self.popularity = pSubmission.score  #number of upvotes

        self.comments = []
        # setting Submissions comments
        i = 0
        for comment in pSubmission.comments:
            if not (isinstance(comment, MoreComments)) and ('I am a bot' not in comment.body):
                self.comments.append(Comment(comment))
                i += 1
            if i >= comLimit:
                break


class SubmissionCollection:
    def __init__(self, subLimit, comLimit, query, subReddit):
        self.subLimit = subLimit
        self.query = query
        self.subReddit = subReddit

        self.submissions = []
        # setting submissions in the collection
        i = 0
        for submission in reddit.subreddit(subReddit).search(query):
            self.submissions.append(Submission(submission, comLimit))
            i += 1
            if i >= subLimit:
                break

        # Text processing (tokenization and stopword removal)
        # Submission title processing
        for sub in self.submissions:
            sub.title = preProcess(sub.title)
            # Comments content processing
            for comment in sub.comments:
                comment.body = preProcess(comment.body)

    def getCommentLengthAverage(self):
        comLengthList = []
        for sub in self.submissions:
            comLengthSum = 0
            for com in sub.comments:
                comLengthSum += len(com.body)

            if len(sub.comments) == 0:
                comLengthList.append(-1)
            else:
                comLengthList.append(comLengthSum / len(sub.comments))
        return comLengthList




def main():
    # nltk.download('stopwords')
    # nltk.download('punkt')
    # nltk.download('wordnet')
    print("Climate Change News Analysis. Discovering Arguments")
    query = input("Enter a query : ")
    subReddit = input("What subreddit do you want to browse (type 'all' for browsing everything): ")
    subLimit = int(input("How much submissions do you want to process: "))
    comLimit = int(input("How much comments per submissions do you want to process: "))
    print("Processing request... \n")

    start_time = time.time()
    subColl = SubmissionCollection(subLimit, comLimit, query, subReddit)
    print("\nExecution time for " + str(subLimit) + " submissions, with " + str(comLimit) + " comments each : " + str(
        (time.time() - start_time)) + " seconds")
    print("List of averge comment's length : " + str(subColl.getCommentLengthAverage()))
    print("\n")

    out = calculateJacquard(subColl)
    print(out)

    return out


subColl = main()
