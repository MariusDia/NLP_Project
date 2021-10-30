from collections import defaultdict

import nltk
import pandas as pd

from nltk.parse import stanford
from text_process import preProcess
import stanza
from empath import Empath
import spacy
from spacy.symbols import *
from spacy.matcher import DependencyMatcher
from spacy import displacy

def find_noun(token):
    if (token):
        return


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
    for sub in subColl:
        for sent in preProcess(sub.comments_doc)[0]:
            doc = nlp(sent)
            for token in doc:
                if token.pos == NOUN:
                    if any(child.text in negative_list for child in token.children):
                        negative_hist[token.text] += 1
                    if token.head.pos == VERB and any(child.text in negative_list for child in token.head.children):
                        negative_hist[token.text] += 1

    print(negative_hist)