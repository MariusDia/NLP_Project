# -*- coding: utf-8 -*-

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer


# Text processing (tokenization, stop words removal)
def preProcess(doc):
    """

    Parameters
    ----------
    doc : List of String
        A document to process.

    Returns the processed document : [0]: a list of words from the basic sentences; [1]: list of tokenized words; [2]: a string of of tokenized words.
    -------
    TYPE
        Process and return a document (tokenization, lemmatization, stop-word removal).

    """
    Stopwords = list(set(nltk.corpus.stopwords.words('english')))
    stemmer = SnowballStemmer("english")
    WN_lemmatizer = WordNetLemmatizer()

    sentences = sent_tokenize(doc)
    tokens = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [stemmer.stem(word) for word in words]
        words = [WN_lemmatizer.lemmatize(word, pos="v") for word in words]

        words = [word for word in words if word.isalpha() and word not in Stopwords]  # get rid of numbers and Stopwords
        tokens.extend(words)

    return sentences,tokens,' '.join(tokens)