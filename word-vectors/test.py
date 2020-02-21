from gensim.models import KeyedVectors, TranslationMatrix
from gensim.test.utils import datapath

model_en = KeyedVectors.load_word2vec_format(datapath("EN.1-10.cbow1_wind5_hs0_neg10_size300_smpl1e-05.txt"))
model_it = KeyedVectors.load_word2vec_format(datapath("IT.1-10.cbow1_wind5_hs0_neg10_size300_smpl1e-05.txt"))

word_pairs = [
    ("one", "uno"), ("two", "due"), ("three", "tre"), ("four", "quattro"), ("five", "cinque"),
    ("seven", "sette"), ("eight", "otto"),
    ("dog", "cane"), ("pig", "maiale"), ("fish", "cavallo"), ("birds", "uccelli"),
    ("apple", "mela"), ("orange", "arancione"), ("grape", "acino"), ("banana", "banana")
]

trans_model = TranslationMatrix(model_en, model_it, word_pairs=word_pairs)

tr = trans_model.translate(["man"], topn=3)

print(tr)
