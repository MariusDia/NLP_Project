# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

import praw
from praw.models import MoreComments, Submission

from text_process import preProcess

from histograms import separateOverlapSubCommentHists
from histograms import mixedOverlapSubCommentHists

from agreement_histograms import mixedAgreeHists
from agreement_histograms import separatedAgreeHists

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
        self.raw_comments = [c.body for c in sorted(pSubmission.comments.list(), key= lambda c: c.score, reverse=True)[0:com_limit]]
        self.raw_article = self.get_raw_article()
        self.comments = [preProcess(c)[2] for c in self.raw_comments if ('I am a bot' not in c)]
        self.article = preProcess(self.raw_article)[2]
        self.comments_doc= "".join(self.raw_comments)

    def get_raw_article(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text,features="html.parser")
        return soup.get_text().strip()


class SubmissionCollection:
    def __init__(self, subLimit, comLimit, query, subReddit):
        self.subLimit = subLimit
        self.query = query
        self.subReddit = subReddit

        self.submissions = []
        # setting submissions in the collection
        i = 0
        for submission in reddit.subreddit(subReddit).search(query, sort="top"):
            if not submission.is_self and submission.num_comments > 15 and not submission.is_video:
                submission.comments.replace_more(limit=None)
                self.submissions.append(SimpleSubmission(submission, comLimit))
                i += 1
                if i >= subLimit:
                    break

        # Text processing (tokenization and stopword removal)
        # Submission title processing
        '''for sub in self.submissions:
            _, _, sub.title = preProcess(sub.title)
            # Comments content processing
            """for comment in sub.comments:
                comment.body = preProcess(comment.body)"""'''

    def getCommentLengthAverage(self):
        '''

        Returns a list of average of the comments' length of each submission
        -------
        comLengthList : list of int
            a list of average of the comments' length of each submission.

        '''
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
