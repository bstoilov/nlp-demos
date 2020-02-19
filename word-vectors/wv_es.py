from gensim.models import Word2Vec
from multiprocessing import cpu_count
import logging
from gensim.utils import save_as_line_sentence
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

es_train_data = '/home/kashon/Downloads/corpus'
es_model_file = '../models/wv_es/wv_es'

class EsCorpus(object):
    def __iter__(self):
        with open(es_train_data) as fp:
            # head = [next(fp) for x in range(50)]
            for line in fp:
                try:
                    yield line.split()
                except Exception as e:
                    pass
                    print('error', line)
                    print(e)


c = EsCorpus()

corpus_fname = 'corpus_es'
# save_as_line_sentence(c, corpus_fname)
w2v = Word2Vec(corpus_file=corpus_fname, size=100, window=5, min_count=5, workers=cpu_count(), iter=5)
w2v.save(es_model_file)