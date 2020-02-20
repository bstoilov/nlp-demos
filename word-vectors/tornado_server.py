from tornado import ioloop
from tornado import web
from tornado import wsgi
from tornado import escape
import logging
import gensim.downloader as api
from gensim.models import KeyedVectors, TranslationMatrix
import numpy as np

vector_top_n = 10
wv_es = '../models/wv_es/wv_es'
wv_bg = '../models/wv_bg/wv_bg'
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

word_pairs = [
    ("едно", "one"), ("две", "two"), ("три", "three"), ("четири", "four"), ("пет", "five"),
    ("шест", "six"), ("седем", "seven"),
    ("куче", "dog"), ("риба", "fish"), ("птици", "birds"),
    ("ябълка", "apple"), ("портокал", "orange"), ("грозде", "grape"), ("банан", "banana")
]


class WordVectorProcessor:

    def __init__(self):
        self.word_vectors_en = api.load("glove-wiki-gigaword-100")
        self.word_vectors_bg = KeyedVectors.load(wv_bg, mmap='r')
        self.translation_mat = TranslationMatrix(self.word_vectors_bg.wv, self.word_vectors_en.wv,
                                                 word_pairs=word_pairs)
        self.word_vectors_bg.wv.most_similar(positive=['крал'], negative=[], topn=vector_top_n)
        self.word_vectors_en.wv.most_similar(positive=['man'], negative=[], topn=vector_top_n)
        logging.info('Word vectors were loaded and initialized')

    def wv_similar(self, body):
        lang = body['lang']
        pos = body['positive']
        neg = body['negative']
        vectors = self.get_vector_model(lang)
        try:
            result = vectors.wv.most_similar(positive=pos, negative=neg, topn=vector_top_n)
        except Exception as e:
            return {'error': str(e).replace('"', '')}

        word_map = {}
        for v in result:
            word_map[v[0]] = v[1]

        return {'words': word_map}

    def translate(self, body):
        word = body['word']

        transl = self.translation_mat.translate([word])
        print(transl)
        return transl

    def get_vector_model(self, lang):
        if lang == "en":
            return self.word_vectors_en
        return self.word_vectors_bg


port = 10001

word_vector_processor = WordVectorProcessor()


class WvHandler(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    def post(self):
        data = escape.json_decode(self.request.body)
        response = word_vector_processor.wv_similar(data)
        logging.info('words resp ' + str(response))
        self.write(response)


class TranslateHandler(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    def post(self):
        data = escape.json_decode(self.request.body)
        response = word_vector_processor.translate(data)
        self.write(response)


endpoints = [
    (r"/words", WvHandler),
    (r"/translate", TranslateHandler)
]

logging.info('Endpoints:')
for e in endpoints:
    logging.info(e[0])

app = web.Application(endpoints)
app.listen(port)
logging.info('Word vector service listening at port ' + str(port))
ioloop.IOLoop.current().start()
