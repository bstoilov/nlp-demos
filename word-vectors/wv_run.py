from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

wv_file = '/home/kashon/Downloads/SBW-vectors-300-min5.bin.gz'
sp_wv_file = '/home/kashon/Downloads/keyed_vectors/complete.kv'

word_vectors = KeyedVectors.load(sp_wv_file, mmap='r')

# vec = word_vectors.get_vector("amor")

vec = word_vectors.get_vector("uno")

topn_n = word_vectors.most_similar(positive=[vec], topn=5)

# topn_n = word_vectors.most_similar(positive=['amor'], negative=[], topn=20)

print(topn_n)
