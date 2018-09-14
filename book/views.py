from nameko.rpc import rpc
from book.models import Book

class DjangoService(object):
    name = "book_service"

    @rpc
    def first_book(self):
        return Book.objects.first().title

    @rpc
    def last_book(self):
        return Book.objects.last().title

    @rpc
    def save_book(self, title, author):
        book = Book()
        book.title = title
        book.author = author
        book.save()
