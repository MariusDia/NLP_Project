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

    for word in sub.article.content.split():
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
    for word in subColl.submissions[subNum].comments[comNum].body.split():
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
        for word in com.body.split():
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

        print(subWords)
        print(subComWords)

        commonWords = list(set(subWords).intersection(subComWords))
        distinctWords = list(set(subWords + subComWords))

        coefficients.append(len(commonWords) / len(distinctWords))
    return coefficients


def calculateJacquard(l1, l2):
    return l1 / l2
