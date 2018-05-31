
from collections import defaultdict, Counter
from uuid import uuid4


class Service:
    def __init__(self):
        self.url_table = defaultdict()
        self.access_table = Counter()

    def shorten(self, url):
        key = str(uuid4())
        self.url_table[key] = url
        print("Here is the key for {0}, {1}".format(url, key))
        return key

    def retrieve(self, key):
        url = self.url_table[key]
        self.access_table[key] += 1
        print('Open {0}'.format(url))


service = Service()
key = service.shorten('https://scholar.google.com/')
service.retrieve(key)
