from collections import defaultdict

import pandas as pd

from text_process import preProcess

import spacy
from spacy.symbols import *

'''

Parameters ----------
subColl : SubmissionCollection A Submission Collection listing every submission and its attributes. 

lexicon : text document, providing words and sentiment value, optional Document from which to extract the 
list of negative sentiment words, it defaults with "vader" lexicon, already provided, but can accept any lexicon with 
a "sentiment" value column 


-------
Returns the histogram of the 10 most negatively referenced noun entities. An entity is considered negatively referenced
when a parser tree presents a direct connection between it and a word listed in the negative list

'''


def negative_entities(subColl, lexicon="lexicons/vader_lexicon.txt"):
    # list of negative words
    doc = pd.read_csv(lexicon, sep='\t', names=['token', 'mn', 'std', 'raw'])
    negative_list = doc[doc['mn'] < -0.5]['token'].tolist()

    # histogram of negative words
    negative_hist = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")
    for sub in subColl.submissions:
        for sent in preProcess(sub.comments_doc)[0]:
            doc = nlp(sent)
            for token in doc:
                if token.pos == NOUN:
                    if any(child.text in negative_list for child in token.children):
                        negative_hist[token.text] += 1
                    if token.head.pos == VERB and any(child.text in negative_list for child in token.head.children):
                        negative_hist[token.text] += 1

    negative_hist = sorted(negative_hist.items(), reverse=True)
    df = pd.DataFrame(negative_hist, columns=['entity name', 'count'])
    df = df.sort_values(by='count', ascending=False)

    fig = df.head(10).plot(kind='bar',
                           title="histogram of the 10 most mentioned entities"
                           , x='entity name'
                           , y='count'
                           , rot=30
                           , legend=True)
    print(df.head(10))
    return fig.get_figure()
