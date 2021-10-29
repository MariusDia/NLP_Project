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
        df =  pd.DataFrame(agreeDict)
        fig = df.plot(kind='bar'
                      , title="histgrams of agreement/disagreement words count of\nevery comments of the submission combined"
                      , x='Agreement/Disagreement Act'
                      , y='count'
                      , rot=0
                      , legend=True)
        figList.append(fig.get_figure())
        
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
    
    # ♣Figure initialization
    if comLimit<len(comsAgreeCount):
        nrows_p = comLimit
    else:
        nrows_p = len(comsAgreeCount)
        
    fig, axs = plt.subplots(nrows = nrows_p)
    fig.suptitle("Agreement/disagreement word count of EACH of the\nfirst " + str(comLimit) + " comments of a submission.")
    
    i=0
    for comAgreeCount in comsAgreeCount:
        df = pd.DataFrame(comAgreeCount)
        df.plot(ax=axs[i]
                , kind='bar'
                , x='Agreement/Disagreement Act'
                , y='count'
                , rot=20
                )
        i+=1
        if i>=5:
            break
    
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
        figList.append(separatedAgreeHist(comsAgreeCount).get_figure())
        
    return figList
        