import gensim.downloader as api
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = api.load("glove-wiki-gigaword-100")

print(model.most_similar("glass"))
vec = model["glass"]

print(len(vec))