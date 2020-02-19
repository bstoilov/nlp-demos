from gensim.models import Word2Vec
from multiprocessing import cpu_count
import logging
from gensim.utils import save_as_line_sentence
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

bg_train_data = '/media/kashon/Local disc/datasets/wv_train'
bg_model_file = '../models/wv_bg/wv_bg'


class BgCorpus(object):
    def __iter__(self):
        with open(bg_train_data) as fp:
            # head = [next(fp) for x in range(50)]
            for line in fp:
                try:
                    yield line.split()
                except Exception as e:
                    pass
                    print('error', line)
                    print(e)


c = BgCorpus()

corpus_fname = 'corpus_bg'
# save_as_line_sentence(c, corpus_fname)
w2v = Word2Vec(corpus_file=corpus_fname, size=100, window=5, min_count=5, workers=cpu_count(), iter=5)
w2v.save(bg_model_file)