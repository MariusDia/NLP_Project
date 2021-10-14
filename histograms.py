# Histogram drawing of Word Overlapping for a sub and its comments separated

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
    # ♣Figure initialization
    # Sublopts count = comments count
    fig, axs = plt.subplots(len(comWordCountList))
    fig.suptitle('Stacked subplots, submission counting/comment counting')
    i = 0
    # Sub plots input
    for comCount in comWordCountList:
        print(str(i) + "  " + str(len(comWordCountList)))
        axs[i].bar(list(subWordCount.keys()), subWordCount.values(), color='b')
        axs[i].bar(list(comCount.keys()), comCount.values(), color='g')
        i += 1


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
        if len(comWordCountList) < 5:
            print("not much comments on this post : " + subColl.submissions[subNum].title)
        if len(comWordCountList) > 1:
            subWordCount = getSubWordCounting(subColl, subNum, subWordLimit)
            separateSubCommentsHist(subWordCount, comWordCountList)
        else:
            print("No comments ? " + str(subColl.submissions[subNum].title))


# Histogram drawing of Word Overlapping for a sub and its comments separated7

subWordLimit = 10
comWordLimit = 10


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