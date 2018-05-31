
from collections import defaultdict, Counter
from uuid import uuid4


class Service:
    def __init__(self):
        self.url_table = defaultdict()
        self.access_table = Counter()

    def shorten(self, url):
        key = str(uuid4())
        self.url_table[key] = url
        return key

    def retrieve(self, key):
        url = self.url_table[key]
        open(url)


service = Service()
key = service.shorten(
    'https://www.careercup.com/page?pid=object-oriented-design-interview-questions')
service.retrieve(key)
