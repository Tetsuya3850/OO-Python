# Book Reader holds multiple books.
# Choose a book to read.
# Access online store to buy new book.

from collections import defaultdict
import copy


class BookReader:
    def __init__(self, book_store):
        self.library = defaultdict()
        self.book_store = book_store

    def access_store(self):
        print("Here are the available titles")
        self.book_store.show_books()

    def buy_book(self, title):
        book = self.book_store.deliver_book(title)
        self.library[book.title] = book

    def read_book(self, title):
        self.library[title].read()


class Book:
    def __init__(self, id, title, author, content):
        self.id = id
        self.title = title
        self.author = author
        self.content = content

    def read(self):
        print(self.content)


class BookStore:
    id = 0

    def __init__(self):
        self.books = defaultdict()
        self.title_id_lookup = defaultdict()
        self.add_book('Harry Potter', 'J. K. Rawling', 'Avadakadabra!')
        self.add_book('The Wind Rises', 'Hayao Miyazaki', 'Zero!')

    def add_book(self, title, author, content):
        self.books[self.id] = Book(self.id, title, author, content)
        self.title_id_lookup[title] = self.id
        self.id += 1

    def show_books(self):
        for book in self.books.values():
            print(book.title)

    def deliver_book(self, title):
        if title in self.title_id_lookup:
            id = self.title_id_lookup[title]
            return copy.deepcopy(self.books[id])


bookStore = BookStore()
bookReader = BookReader(bookStore)
bookReader.access_store()
bookReader.buy_book('The Wind Rises')
bookReader.read_book('The Wind Rises')
