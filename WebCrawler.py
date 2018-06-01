
from collections import deque, defaultdict
from functools import reduce


class Page:
    def __init__(self, id, contents):
        self.id = id
        self.contents = contents
        self.link_pages = []

    def add_link(self, pages):
        self.link_pages.append(pages)


A = Page('a', 'Birds fly. Fishes swim. Drink beer')
B = Page('b', 'I am so tired. Give me a beer')
C = Page('c', 'My favorite food is sushi and beer')
D = Page('d', 'Drink water when hot outside')
E = Page('e', 'Save the world make it a better place with sushi')
A.add_link(B)
A.add_link(C)
C.add_link(A)
C.add_link(D)
D.add_link(E)
E.add_link(B)


class WebCrawler:
    def __init__(self):
        self.crolled_pages = set()
        self.uncrolled_pages = deque()
        self.index = ReverseIndexService()
        self.info = DocumentService()
        self.cache = CacheService()

    def add_page_to_crawl(self, page):
        self.uncrolled_pages.append(page)

    def crawl(self):
        while self.uncrolled_pages:
            next_page = self.uncrolled_pages.popleft()
            self.index.build_index(next_page)
            self.info.add_document(next_page)
            for page in next_page.link_pages:
                if page not in self.crolled_pages:
                    self.uncrolled_pages.append(page)
            self.crolled_pages.add(next_page)

    def search(self):
        print("What to search?")
        qs = input()
        if self.cache.in_cache(qs):
            match = self.cache.retrieve_cache(qs)
        else:
            match = self.index.query(qs)
            self.cache.add_cache(qs, match)
        if not match:
            print("No match")
        for id in match:
            print(self.info.document[id])


class ReverseIndexService:
    def __init__(self):
        self.reverse_index = defaultdict(list)

    def build_index(self, page):
        words = set([word.strip(",.")
                     for word in page.contents.lower().split()])
        for word in words:
            self.reverse_index[word].append(page.id)

    def query(self, qs):
        candid_pages = []
        q_words = [word.strip(",.") for word in qs.lower().split()]
        for word in q_words:
            if word in self.reverse_index:
                candid_pages.append(self.reverse_index[word])
        if not candid_pages:
            return []
        return reduce(self.get_intersection, iter(candid_pages))

    def get_intersection(self, A, B):
        A.sort()
        B.sort()
        i = 0
        j = 0
        result = []
        while i < len(A) and j < len(B):
            if A[i] == B[j]:
                if i == 0 or A[i] != A[i-1]:
                    result.append(A[i])
                i += 1
                j += 1
            elif A[i] < B[j]:
                i += 1
            else:
                j += 1
        return result


class DocumentService:
    def __init__(self):
        self.document = defaultdict()

    def add_document(self, page):
        self.document[page.id] = page.contents


class CacheService:
    def __init__(self):
        self.cache = defaultdict()

    def add_cache(self, qs, result):
        self.cache[qs] = result

    def in_cache(self, qs):
        return qs in self.cache

    def retrieve_cache(self, qs):
        return self.cache[qs]


crawler = WebCrawler()
crawler.add_page_to_crawl(A)
crawler.crawl()
crawler.search()
