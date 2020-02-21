from tornado import ioloop
from tornado import web
from tornado import escape
import logging
from gensim.models import KeyedVectors
import numpy as np
import requests
import chardet
from scipy import spatial

vector_top_n = 10
wv_bg = '../models/wv_bg/wv_bg'
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'


class WordVectorProcessor:

    def __init__(self):
        self._load_wv()

    def _load_wv(self):
        self.word_vectors_bg = KeyedVectors.load(wv_bg, mmap='r')
        self.word_vectors_bg.wv.most_similar(positive=['крал'], negative=[], topn=vector_top_n)
        logging.info('Word vectors were loaded and initialized')

        self.headers = {
            'user-agent': user_agent,
            'accept-encoding': 'gzip, deflate, br',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9,bg;q=0.8'
        }


    def wv_similar(self, body):
        pos = body['positive']
        neg = body['negative']
        vectors = self.word_vectors_bg
        try:
            result = vectors.wv.most_similar(positive=pos, negative=neg, topn=vector_top_n)
        except Exception as e:
            return {'error': str(e).replace('"', '')}

        word_map = {}
        for v in result:
            word_map[v[0]] = v[1]

        return {'words': word_map}

    def extract_same(self, body):
        url = body['url']
        group = body['group']
        conetnts = self.download_page(url=url)
        return self.belong(group.split(" "), conetnts.split(" "))

    def belong(self, group, targets, sim_factor=0.5):
        group_vectors = []
        for item in group:
            group_vectors.append(self.word_vectors_bg.wv[item])

        belonging = []
        for target in targets:
            if target not in self.word_vectors_bg.wv:
                continue
            target_vec = self.word_vectors_bg.wv[target]
            for group_vec in group_vectors:
                cosine_dist = spatial.distance.cosine(target_vec, group_vec)
                sim = 1 - cosine_dist
                if sim >= sim_factor:
                    belonging.append(target)
                    break
        belonging = list(dict.fromkeys(belonging))
        return {"items": belonging}

    def download_page(self, url):
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            charset = chardet.detect(response.content)['encoding']
            result_text = response.content.decode(charset)
            return result_text

        return ""

    def similarity(self, body):
        first_vec = self.get_sentence_vector(body['first'].lower())
        second_vec = self.get_sentence_vector(body['second'].lower())

        if not type(first_vec) is list or not type(second_vec) is list:
            return {'similarity': 0}

        cosine_dist = spatial.distance.cosine(first_vec, second_vec)
        sim = 1 - cosine_dist
        if sim < 0:
            sim = 0
        elif sim > 1:
            sim = 1

        return {'similarity': sim}


    def get_sentence_vector(self, sentence):
        vecs = []
        for w in sentence.split():
            if w in self.word_vectors_bg.wv:
                vecs.append(self.word_vectors_bg.wv[w])
            else:
                pass
                # logging.warning(w + ' not in vocab')
        data = np.array(vecs)
        avg = np.average(data, axis=0)
        return avg.tolist()


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


class GroupHandler(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    def post(self):
        data = escape.json_decode(self.request.body)
        response = word_vector_processor.extract_same(data)
        self.write(response)


class SimilarityHandler(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    def post(self):
        data = escape.json_decode(self.request.body)
        response = word_vector_processor.similarity(data)
        self.write(response)


endpoints = [
    (r"/words", WvHandler),
    (r"/belong", GroupHandler),
    (r"/similarity", SimilarityHandler),
]

logging.info('Endpoints:')
for e in endpoints:
    logging.info(e[0])

app = web.Application(endpoints)
app.listen(port)
logging.info('Word vector service listening at port ' + str(port))
ioloop.IOLoop.current().start()
