
from wordcount import *
import gensim
from gensim import corpora
from nltk.tokenize import sent_tokenize, word_tokenize


def performLDA(subColl, NUM_TOPICS=3, ):
    jc = []
    for sub in subColl.submissions:
        article_text_data = [word_tokenize(sub.article.content)]
        dictionary = corpora.Dictionary(article_text_data)
        corpus = [dictionary.doc2bow(text) for text in article_text_data]
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
        article_topics = ldamodel.show_topics(num_words=5, formatted=False)
        article_topic_words = set()
        for topic in article_topics:
            article_topic_words = article_topic_words.union(set([t[0] for t in topic[1]]))

        comments_text_data = []
        for comment in sub.comments:
            body = comment.body
            comments_text_data.append(word_tokenize(body))
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
