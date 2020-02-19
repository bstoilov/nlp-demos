import tornado.ioloop
import tornado.web
import tornado.wsgi
import logging
from gensim.models import KeyedVectors
import numpy as np

vector_top_n = 10
wv_file = '../models/wv_bg/wv_bg'
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class WordVectorProcessor:

    def __init__(self):
        self.word_vectors = KeyedVectors.load(wv_file, mmap='r')
        self.word_vectors.most_similar(positive=['крал'], negative=[], topn=vector_top_n)
        logging.info('Word vectors were loaded and initialized')

    def wv_similar(self, body):
        pos = body['positive']
        neg = body['negative']

        try:
            result = self.word_vectors.most_similar(positive=pos, negative=neg, topn=vector_top_n)
        except Exception as e:
            return {'error': str(e).replace('"', '')}

        word_map = {}
        for v in result:
            word_map[v[0]] = v[1]

        return {'words': word_map}

    def get_vector(self, body):
        word_vec = self.word_vectors.wv[body['word']]
        print(word_vec)
        return {'vector': " ".join(map(str, word_vec))}

    def get_word_by_vector(self, body):
        vec = []
        for w in str(body['vec']).split(" "):
            vec.append(float(w))
        print(vec)
        res = self.word_vectors.most_similar(positive=[vec], negative=[], topn=vector_top_n)
        return res


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


class VectorHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        response = word_vector_processor.get_word_by_vector(data)
        self.write(response)


class VecToWordHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        response = word_vector_processor.get_word_by_vector(data)
        self.write(response)


endpoints = [
    (r"/words", WvHandler),
    (r"/vector", VectorHandler),
    (r"/vec2word", VecToWordHandler)
]

logging.info('Endpoints:')
for e in endpoints:
    logging.info(e[0])

app = tornado.web.Application(endpoints)
app.listen(port)
logging.info('Word vector service listening at port ' + str(port))
tornado.ioloop.IOLoop.current().start()
