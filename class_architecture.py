# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

import praw
from praw.models import MoreComments, Submission

from text_process import preProcess

# Reddit API authentification
reddit = praw.Reddit(
    client_id="9aC2iDzQQi04w-q1cPmjUw",
    client_secret="O29M5Puueuew1y_rDYVuvUZLdKuF_w",
    user_agent="NLP_Project_API/0.0.1",
)


# -----------Class architecture---------------
class SimpleSubmission():
    def __init__(self, pSubmission, com_limit):
        self.title = pSubmission.title
        self.url = pSubmission.url
        self.is_self = pSubmission.is_self
        self.raw_comments = [c.body for c in pSubmission.comments.list()[0:com_limit]]
        self.raw_article = self.get_raw_article()
        self.comments = [preProcess(c)[2] for c in self.raw_comments if ('I am a bot' not in c)]
        self.article = preProcess(self.raw_article)[2]

    def get_raw_article(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text)
        return soup.get_text().strip()


class SubmissionCollection:
    def __init__(self, subLimit, comLimit, query, subReddit):
        self.subLimit = subLimit
        self.query = query
        self.subReddit = subReddit

        self.submissions = []
        # setting submissions in the collection
        i = 0
        for submission in reddit.subreddit(subReddit).search(query):
            if not submission.is_self and submission.num_comments > 0:
                submission.comments.replace_more(limit=0)
                self.submissions.append(SimpleSubmission(submission, comLimit))
                i += 1
                if i >= subLimit:
                    break

        # Text processing (tokenization and stopword removal)
        # Submission title processing
        for sub in self.submissions:
            _, _, sub.title = preProcess(sub.title)
            # Comments content processing
            """for comment in sub.comments:
                comment.body = preProcess(comment.body)"""

    def getCommentLengthAverage(self):
        comLengthList = []
        for sub in self.submissions:
            comLengthSum = 0
            for com in sub.comments:
                comLengthSum += len(com)

            if len(sub.comments) == 0:
                comLengthList.append(-1)
            else:
                comLengthList.append(comLengthSum / len(sub.comments))
        return comLengthList
