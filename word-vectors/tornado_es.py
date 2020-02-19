import tornado.ioloop
import tornado.web
import tornado.wsgi
import logging
from gensim.models import KeyedVectors
import numpy as np

vector_top_n = 10
wv_file = '../models/wv_es/wv_es'
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class WordVectorProcessor:

    def __init__(self):
        self.word_vectors = KeyedVectors.load(wv_file, mmap='r')
        self.word_vectors.most_similar(positive=['amigo'], negative=[], topn=vector_top_n)
        logging.info('Word vectors were loaded and initialized')

    def get_sentence_vector(self, sentence):
        vecs = []
        for w in sentence.split():
            if w in self.word_vectors.wv:
                vecs.append(self.word_vectors.wv[w])
            else:
                pass
                # logging.warning(w + ' not in vocab')
        data = np.array(vecs)
        avg = np.average(data, axis=0)
        return avg.tolist()

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
        vectors = []

        for s in body['sentances']:
            vec = self.get_sentence_vector(s)
            if type(vec) != list:
                vec = None

            vectors.append(vec)

        return {'vectors': vectors}


port = 10002

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
        response = word_vector_processor.get_vector(data)
        self.write(response)


endpoints = [
    (r"/words", WvHandler),
    (r"/vector", VectorHandler),
]

logging.info('Endpoints:')
for e in endpoints:
    logging.info(e[0])

app = tornado.web.Application(endpoints)
app.listen(port)
logging.info('Word vector service listening at port ' + str(port))
tornado.ioloop.IOLoop.current().start()
