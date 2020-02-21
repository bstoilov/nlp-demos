from gensim.models import Word2Vec
from multiprocessing import cpu_count
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

bg_model_file = '../models/wv_bg/wv_bg1'

# 1 855 947 unique tokens
corpus_fname = 'corpus_bg'
w2v = Word2Vec(corpus_file=corpus_fname, size=100, window=5, min_count=5, workers=cpu_count(), iter=5)
w2v.save(bg_model_file)