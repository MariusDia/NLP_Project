from wordcount import *
import gensim
from gensim import corpora
from nltk.tokenize import sent_tokenize, word_tokenize


def performLDA(subColl, NUM_TOPICS=3, ):
    for sub in subColl.submissions:
        print(f'sub: {sub}')
        text_data = [word_tokenize(sub.article.content)]
        print((text_data))
        dictionary = corpora.Dictionary(text_data)
        corpus = [dictionary.doc2bow(text) for text in text_data]

        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
        ldamodel.save('model5.gensim')
        topics = ldamodel.print_topics(num_words=5)
        for topic in topics:
            print(topic)
    return 0