# -*- coding: utf-8 -*-

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

# Text processing (tokenization, stop words removal)
def preProcess(doc):
    Stopwords = list(set(nltk.corpus.stopwords.words('english')))
    stemmer = SnowballStemmer("english")
    WN_lemmatizer = WordNetLemmatizer()

    sentences = sent_tokenize(doc)
    Tokens = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [stemmer.stem(word) for word in words]
        words = [WN_lemmatizer.lemmatize(word, pos="v") for word in words]

        words = [word for word in words if word.isalpha() and word not in Stopwords]  # get rid of numbers and Stopwords
        Tokens.extend(words)

    return ' '.join(Tokens)

def sentenceProcess(doc):
    sentences = sent_tokenize(doc)
    return sentences

