
from collections import defaultdict, Counter
from random import choice, randrange


class Proxy:
    def __init__(self):
        self.read_services = []
        self.write_services = []

    def add_read_service(self, read_service):
        self.read_services.append(read_service)

    def add_write_service(self, write_service):
        self.write_services.append(write_service)

    def read(self, key):
        read_service = choice(self.read_services)
        read_service.retrieve(key)

    def write(self, url):
        write_service = choice(self.write_services)
        return write_service.shorten(url)


class DB:
    def __init__(self):
        self.url_table = defaultdict()
        self.access_table = Counter()


class ReadService:
    def __init__(self, db):
        self.db = db

    def retrieve(self, key):
        url = self.db.url_table[key]
        self.db.access_table[key] += 1
        print('Open {0}'.format(url))


class WriteService:
    def __init__(self, db):
        self.db = db

    def key_generator(self):
        string = 'abcdefghijklmnopqrstuvwxyz0123456789'
        result = []
        for _ in range(7):
            result.append(string[randrange(len(string))])
        return "".join(result)

    def shorten(self, url):
        key = self.key_generator()
        while key in self.db.url_table:
            key = self.key_generator()
        self.db.url_table[key] = url
        print("Here is the key for {0}, {1}".format(url, key))
        return key


proxy = Proxy()
db = DB()
read_service_1 = ReadService(db)
read_service_2 = ReadService(db)
proxy.add_read_service(read_service_1)
proxy.add_read_service(read_service_2)
write_service_1 = WriteService(db)
proxy.add_write_service(write_service_1)
key = proxy.write('https://scholar.google.com/')
proxy.read(key)
