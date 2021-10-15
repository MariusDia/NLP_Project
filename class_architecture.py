# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

import praw
from praw.models import MoreComments

from text_process import preProcess, sentenceProcess

# Reddit API authentification
reddit = praw.Reddit(
    client_id="9aC2iDzQQi04w-q1cPmjUw",
    client_secret="O29M5Puueuew1y_rDYVuvUZLdKuF_w",
    user_agent="NLP_Project_API/0.0.1",
)

# -----------Class architecture---------------

class Comment:
    def __init__(self, pComment):
        self.body = pComment.body


class Article:
    def __init__(self, url):
        self.url = url
        

class PreProcessArticle(Article):
    def __init__(self, url):
        super().__init__(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.text)
        self.content = preProcess(soup.get_text().strip())

class SentenceProcessArticle(Article):
    def __init__(self, url):
        super().__init__(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.text)
        self.content = sentenceProcess(soup.get_text().strip())

# Simplified version of praw Submission class model
class Submission:

    def __init__(self, pSubmission, comLimit):
        self.title = pSubmission.title
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

class PreProcessSubmission(Submission):
    def __init__(self, pSubmission, comLimit):
        super().__init__(pSubmission, comLimit)
        self.article = PreProcessArticle(pSubmission.url)

class SentenceProcessSubmission(Submission):
    def __init__(self, pSubmission, comLimit):
        super().__init__(pSubmission, comLimit)
        self.article = SentenceProcessArticle(pSubmission.url)

class SubmissionCollection:
    def __init__(self, subLimit, comLimit, query, subReddit):
        self.subLimit = subLimit
        self.query = query
        self.subReddit = subReddit
        self.comLimit = comLimit

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

class PreProcessSubmissionCollection(SubmissionCollection):
    def __init__(self, subLimit, comLimit, query, subReddit):
        super().__init__(subLimit, comLimit, query, subReddit)
        self.submissions = []
        # setting submissions in the collection
        i = 0
        for submission in reddit.subreddit(self.subReddit).search(self.query):
            self.submissions.append(PreProcessSubmission(submission, self.comLimit))
            i += 1
            if i >= self.subLimit:
                break

        # Text processing (tokenization and stopword removal)
        # Submission title processing
        for sub in self.submissions:
            sub.title = preProcess(sub.title)
            # Comments content processing
            for comment in sub.comments:
                comment.body = preProcess(comment.body)

class SentenceProcessSubmissionCollection(SubmissionCollection):
    def __init__(self, subLimit, comLimit, query, subReddit):
        super().__init__(subLimit, comLimit, query, subReddit)
        self.submissions = []
        # setting submissions in the collection
        i = 0
        for submission in reddit.subreddit(self.subReddit).search(self.query):
            self.submissions.append(SentenceProcessSubmission(submission, self.comLimit))
            i += 1
            if i >= self.subLimit:
                break

        # Text processing (tokenization and stopword removal)
        # Submission title processing
        for sub in self.submissions:
            sub.title = sentenceProcess(sub.title)
            # Comments content processing
            for comment in sub.comments:
                comment.body = sentenceProcess(comment.body)