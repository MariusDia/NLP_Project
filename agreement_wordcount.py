#Articles are often denouncing ecological problem, and so comments are also using denouncing terms which can be found in disagreement list...
agreement = ["ok", "yes,", "sure", "agree", "cool", "good", "go", "yeah", "yup", "yep", "absolutely", "exactly"]
disagreement = ["no", "but", "disagree", "suck", "not", "bad", "disapprove"]

def mergedComAgreeCount(subColl, subNum):
    '''

    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.
    subNum : int
        Submission number.

    Returns a dictionary of agreement/disagreement words count of a submission's comments.
    -------
    agreeDict : dict
        A dictionary of agreement/disagreement words count of a submission's comments.

    '''
    agreeDict = {"Agreement/Disagreement Act":["agreement", "disagreement"], "count":[0,0]}
    sub = subColl.submissions[subNum]
    
    for com in sub.comments:
        for word in com.split():
            if word in agreement:
                agreeDict["count"][0]+=1
            elif word in disagreement:
                agreeDict["count"][1]+=1
    
    return agreeDict


def comAgreeCounting(sub):
    '''

    Parameters
    ----------
    sub : SimpleSubmission
        A submission.

    Returns a list of dictionaries storing agreement/disagreement words count of EACH comments of "sub"
    -------
    comsAgreeCount : list of dictionaries
        list of dictionaries storing agreement/disagreement words count of EACH comments of "sub".

    '''
    comsAgreeCount = []
    
    for com in sub.comments:
        agreeDict = {"Agreement/Disagreement Act":["agreement", "disagreement"], "count":[0,0]}
        for word in com.split():
            if word in agreement:
                agreeDict["count"][0]+=1
            elif word in disagreement:
                agreeDict["count"][1]+=1
        comsAgreeCount.append(agreeDict)
        
    return comsAgreeCount