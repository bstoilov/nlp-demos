from tornado import ioloop
from tornado import web
from tornado import wsgi
from tornado import escape
import logging
import gensim.downloader as api
from gensim.models import KeyedVectors, TranslationMatrix
import numpy as np
import requests
import chardet

vector_top_n = 10
wv_es = '../models/wv_es/wv_es'
wv_bg = '../models/wv_bg/wv_bg'
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'


class WordVectorProcessor:

    def __init__(self):
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

        

    def download_page(self, url):
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            charset = chardet.detect(response.content)['encoding']
            result_text = response.content.decode(charset)
            return result_text

        return ""


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


class Kmeans(web.RequestHandler):
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
