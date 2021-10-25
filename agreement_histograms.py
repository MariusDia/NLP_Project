#import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

from agreement_wordcount import mergedComAgreeCount
from agreement_wordcount import comAgreeCounting

def mixedAgreeHists(subColl):
    '''

    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.

    Returns a list of histgrams of agreement/disagreement words count of EVERY comments of EACH submission of subColl
    -------
    figList : List of figures

    '''
    figList = []
    for i in range(len(subColl.submissions)):
        agreeDict = mergedComAgreeCount(subColl, i)
        
        #Putting the previous dictionary into a dtaframe which plots a histogram of word counts
        fig = plt.bar(list(agreeDict.keys()), agreeDict.values())
        #plt.title("Agreement/disagreement word count of EVERY comments of the article '" + subColl.submissions[i].title + "'.")
        figList.append(fig)
        #plt.show()
        
    return figList




def separatedAgreeHist(comsAgreeCount, comLimit=5):
    '''

    Parameters
    ----------
    comsAgreeCount : list of dictionaries
        list of dictionaries storing agreement/disagreement words count of EACH comments of submission.

    Returns a histogram showing agreement/disagreement words count of EACH comments of submission.
    -------
    fig : Figure
        A histogram showing agreement/disagreement words count of EACH comments of a submission.

    '''
    fig, axs = plt.subplots(comLimit)
    fig.suptitle("Agreement/disagreement word count of EACH comments of a submission.")
    for i in range(comLimit):
        axs[i].bar(list(comsAgreeCount[i].keys()),comsAgreeCount[i].values())
    
    return fig

def separatedAgreeHists(subColl):
    '''

    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.

    Returns
    -------
    figList : TYPE
        DESCRIPTION.

    '''
    figList = []
    
    for sub in subColl.submissions:
        comsAgreeCount = comAgreeCounting(sub)
        figList.append(separatedAgreeHist(comsAgreeCount))
        
    return figList
        