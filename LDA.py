from text_process import preProcess
from wordcount import *
import gensim
from gensim import corpora
from nltk.tokenize import sent_tokenize, word_tokenize


def performLDA(subColl, NUM_TOPICS=3, ):
    '''

    Parameters
    ----------
    subColl : SubmissionCollection
        A Submission Collection listing every submission and its attributes.
    NUM_TOPICS : int, optional
        Number of topics the LDA model will create, default is 3.

    Returns the list of jaccard coefficients for each sumbission, calculated between the set of words creating
    N_TOPICS in the article and merged comments

    '''
    jc = []
    for sub in subColl.submissions:
        article_text_data = [preProcess(sub.raw_article)[1]]
        dictionary = corpora.Dictionary(article_text_data)
        corpus = [dictionary.doc2bow(text) for text in article_text_data]
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
        article_topics = ldamodel.show_topics(num_words=5, formatted=False)
        article_topic_words = set()
        for topic in article_topics:
            article_topic_words = article_topic_words.union(set([t[0] for t in topic[1]]))

        comments_text_data= [preProcess(sub.comments_doc)[1]]
        dictionary = corpora.Dictionary(comments_text_data)
        corpus = [dictionary.doc2bow(text) for text in comments_text_data]
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
        comments_topics = ldamodel.show_topics(num_words=5, formatted=False)
        comments_topic_words = set()
        for topic in comments_topics:
            comments_topic_words = comments_topic_words.union(set([t[0] for t in topic[1]]))

        print(article_topic_words)
        print(comments_topic_words)
        jc.append(jacquardCoeff(list(article_topic_words),list(comments_topic_words)))
    return jc
