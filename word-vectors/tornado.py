import tornado.ioloop
import tornado.web
import tornado.wsgi
import logging
from gensim.models import KeyedVectors
import numpy as np

vector_top_n = 10
wv_es = '../models/wv_es/wv_es'
wv_bg = '../models/wv_bg/wv_bg'
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class WordVectorProcessor:

    def __init__(self):
        self.word_vectors_es = KeyedVectors.load(wv_es, mmap='r')
        self.word_vectors_bg = KeyedVectors.load(wv_bg, mmap='r')
        self.word_vectors_bg.most_similar(positive=['крал'], negative=[], topn=vector_top_n)
        self.word_vectors_es.most_similar(positive=['amigo'], negative=[], topn=vector_top_n)
        logging.info('Word vectors were loaded and initialized')

    def wv_similar(self, body):
        lang = body['lang']
        pos = body['positive']
        neg = body['negative']
        vectors = self.word_vectors_bg
        if lang is "es":
            vectors = self.word_vectors_es
        try:
            result = vectors.most_similar(positive=pos, negative=neg, topn=vector_top_n)
        except Exception as e:
            return {'error': str(e).replace('"', '')}

        word_map = {}
        for v in result:
            word_map[v[0]] = v[1]

        return {'words': word_map}

    def translate(self, body):
        source = body['from']
        dest = body['to']
        word = body['word']

        vec = self.get_vector_model(source).wv[word]
        transl = self.get_vector_model(dest).most_similar(positive=[vec], negative=[], topn=vector_top_n)

        return transl

    def get_vector_model(self, lang):
        if lang is "es":
            return self.word_vectors_es
        return self.word_vectors_bg

port = 10001

word_vector_processor = WordVectorProcessor()


class WvHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        response = word_vector_processor.wv_similar(data)
        logging.info('words resp ' + str(response))
        self.write(response)

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


class TranslateHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        response = word_vector_processor.translate(data)
        self.write(response)


endpoints = [
    (r"/words", WvHandler),
    (r"/translate", TranslateHandler)
]

logging.info('Endpoints:')
for e in endpoints:
    logging.info(e[0])

app = tornado.web.Application(endpoints)
app.listen(port)
logging.info('Word vector service listening at port ' + str(port))
tornado.ioloop.IOLoop.current().start()
