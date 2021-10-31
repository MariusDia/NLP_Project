from collections import defaultdict

import pandas as pd

from text_process import preProcess

import spacy
from spacy.symbols import *

def negative_entities(subColl, lexicon="lexicons/vader_lexicon.txt"):
    # nltk.download('averaged_perceptron_tagger')
    # nltk.download('maxent_ne_chunker')
    # nltk.download('words')
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
    df = pd.DataFrame(negative_hist,columns=['entity name','count'])
    df = df.sort_values(by='count', ascending=False)

    fig = df.head(10).plot(kind='bar',
                           title="histogram of the 10 most mentioned entities"
                           , x='entity name'
                           , y='count'
                           , rot=0
                           , legend=True)
    print(df.head(10))
    return fig.get_figure()
