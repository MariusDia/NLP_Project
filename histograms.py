#import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

from wordcount import getSubCommentsWordCounting
from wordcount import getSubWordCounting
from wordcount import getMergedComWordCount

def separateSubCommentsHist(subWordCount, comWordCountList):
    '''

    Parameters
    ----------
    subWordCount : dict
        A dictionary of the "wordLimit" most common words in a submission article.
    comWordCountList : list
        List of dictionaries of the "wordLimit" most common words of every chosen comments of a submission.

    Returns an histogram of word overlapping of ONE SUBMISSION and EACH of its COMMENTS
    -------
    Returns an histogram of word overlapping of ONE SUBMISSION and EACH of its COMMENTS.

    '''

    # ♣Figure initialization
    fig, axs = plt.subplots(nrows = len(comWordCountList))
    fig.suptitle("Word occurences of a submission's linked article and its first comments,\nseperated for each comment")
    i = 0
    
    # Sub plots input
    for comWordCount in comWordCountList:
        
        #Putting word counts in a dictionary
        totalWordCount = {}
        totalWordCount["Art."] = subWordCount
        totalWordCount["Com."] = comWordCount
        
        #Putting the previous dictionary into a dataframe which plots a histogram of word counts
        df = pd.DataFrame(totalWordCount)
        df.plot(ax=axs[i]
                , kind='bar'
                , rot=30)
        
        i += 1
        if i>=5:
            break

    return fig

def separateOverlapSubCommentHists(subColl, subWordLimit=10, comWordLimit=10):
    '''

    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.
    subWordLimit : int, optional
        Select the 'subWordLimit' most common words of SUBMISSION. The default is 10
    comWordLimit : int, optional
        Select the 'comWordLimit' most common words of COMMENTs. The default is 10

    Draws X histograms of word overlapping of EVERY SUBMISSION and EACH of their COMMENTS
    -------
    Returns X histograms of word overlapping of EVERY SUBMISSION and EACH of their COMMENTS.

    '''
    figList = []
    for subNum in range(len(subColl.submissions)):
        comWordCountList = getSubCommentsWordCounting(subColl, subNum, comWordLimit)
        
        #notify if not much comments
        if len(comWordCountList) < 5:
            print("not much comments on this post : " + subColl.submissions[subNum].title)
            return "Not much comments"
        
        #Drawing histograms if there is at least five comments
        if len(comWordCountList) > 4:
            subWordCount = getSubWordCounting(subColl, subNum, subWordLimit)
            figList.append(separateSubCommentsHist(subWordCount, comWordCountList))
            
        #Nothing if there is no comments
        else:
            print("No comments ? " + str(subColl.submissions[subNum].title))
            return "No comments"
        
    return figList


# Histogram drawing of Word Overlapping for a sub and its comments separate
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
    Returns X histograms of word overlapping of EVERY SUBMISSION and EVERY one of their COMMENTS.

    '''
    
    figList = []
    for i in range(len(subColl.submissions)):
        #Getting word counting of article and comments
        subWordCounting = getSubWordCounting(subColl, i, comWordLimit)
        mergedComWordCount = getMergedComWordCount(subColl, i, subWordLimit)
        
        #Putting word counts in a dictionary
        totalWordCount = {}
        totalWordCount["Article Word Counting (total counting: "+ str(sum(subWordCounting.values())) +" )"] = subWordCounting
        totalWordCount["Comments Word Counting (total counting: "+ str(sum(mergedComWordCount.values())) +" )"] = mergedComWordCount
        
        #Putting the previous dictionary into a dtaframe which plots a histogram of word counts
        fig = pd.DataFrame(totalWordCount).plot(kind='bar'
                                                , title="Word occurences of a submission's linked article and its " + str(len(subColl.submissions[i].comments)) + " first comments,\nall comments' words are mixed"
                                                , legend=True
                                                , rot=30)
        
        figList.append(fig.get_figure())
        
    return figList