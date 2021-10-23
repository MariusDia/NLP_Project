import os
from sentistrength import PySentiStr
from text_process import preProcess
from scipy import stats
import numpy as np

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

    # Getting word counting
    sub = subColl.submissions[subNum]

    for word in sub.article.split():
        if word not in subWordCount.keys():
            subWordCount[word] = 1
        else:
            subWordCount[word] += 1

    # Sorting and taking only 10 most common words
    subWordCount = {k: v for k, v in sorted(subWordCount.items(), key=lambda item: item[1], reverse=True)}
    for i in range(len(subWordCount) - wordLimit):
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

    # Getting word counting
    for word in subColl.submissions[subNum].comments[comNum].split():
        if word not in subCommentCount.keys():
            subCommentCount[word] = 1
        else:
            subCommentCount[word] += 1

    # Sorting and taking only 100 most common words of the first comment
    subCommentCount = {k: v for k, v in sorted(subCommentCount.items(), key=lambda item: item[1], reverse=True)}
    for _ in range(len(subCommentCount) - wordLimit):
        subCommentCount.popitem()
    return subCommentCount


# List of word counting dictionaries for every comments of first submission
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

    comWordCountList = []
    sub = subColl.submissions[subNum]
    for i in range(len(sub.comments)):
        comWordCountList.append(getCommentWordCounting(subColl, subNum, i, wordLimit))
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
    sub = subColl.submissions[subNum]
    for com in sub.comments:
        for word in com.split():
            if word not in mergedComWordCount.keys():
                mergedComWordCount[word] = 1
            else:
                mergedComWordCount[word] += 1
    # Sorting and taking only 100 most common words of the first comment
    mergedComWordCount = {k: v for k, v in sorted(mergedComWordCount.items(), key=lambda item: item[1], reverse=True)}
    for _ in range(len(mergedComWordCount) - wordLimit):
        mergedComWordCount.popitem()

    return mergedComWordCount


def calculateJacquard(subColl):
    '''


    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.

    Returns
    -------
    coefficients : list
        A list of of Jaccard indexes between a submission article and its comments.

    '''
    coefficients = []
    for i in range(len(subColl.submissions)):
        subWords = list(getSubWordCounting(subColl, i, 20).keys())
        subComWords = list(getMergedComWordCount(subColl, i, 20).keys())

        coefficients.append(jacquardCoeff(subWords,subComWords))
    return coefficients


def jacquardCoeff(l1, l2):
    '''


    Parameters
    ----------
    l1,l2 : lists
        The two vector for which the j.c. is calculated

    Returns
    -------
    double
    The j.c. value calculated on the lists

    '''
    commonWords = list(set(l1).intersection(l2))
    distinctWords = list(set(l1 + l2))
    return len(commonWords)/len(distinctWords)




def pearsonCorrelation(subColl):
    '''
    
    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.

    Returns the statistical correlation between sentiment associated to original document
    -------

    '''
    
    senti = PySentiStr()
    curr_dir = os.getcwd()
    senti.setSentiStrengthPath(str(curr_dir) + '\SentiStrengthCom.jar')
    senti.setSentiStrengthLanguageFolderPath(str(curr_dir) + '\SentStrength_Data_Sept2011\\')
    pearson_scores = []
    nullScore = (0, 0)
    for sub in subColl.submissions:
        article = sub.raw_article


        #allcomments = [preProcess(com)[0] for com in subColl.submissions[0].raw_comments]
        """ allcomments = subColl.submissions[0].raw_comments
        for com in allcomments:
            com = preProcess(com)[0]
        """
        all_comments = preProcess(sub.comments_doc)[0]
        
        sentiArticles = senti.getSentiment(article, score="dual")
        
        if all_comments == '':
            for i in range(len(sentiArticles)):
                sentiComments.append(nullScore)
        else:
            sentiComments = senti.getSentiment(all_comments, score="dual")
            
        if len(sentiComments) < len(sentiArticles):
            for i in range(len(sentiComments), len(sentiArticles), 1):
                sentiComments.append(nullScore)
        elif len(sentiComments) > len(sentiArticles):
            for i in range(len(sentiArticles), len(sentiComments), 1):
                sentiArticles.append(nullScore)
                
        pearson_scores.append(stats.pearsonr(np.array(sentiArticles).reshape(len(sentiArticles)*2,), np.array(sentiComments).reshape(len(sentiComments)*2,)))
    return pearson_scores