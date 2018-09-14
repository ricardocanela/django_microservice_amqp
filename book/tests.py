from django.test import TestCase
from .models import Book
from .views import DjangoService

# Create your tests here.
class ServiceTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title='title_test', author='author_test')

    def test_first_book(self):
        book = Book.objects.first()
        self.assertEqual(DjangoService.first_book(self), book.title)

    def test_save_book(self):
        title = 'title_test2'
        author = 'author_test2'
        DjangoService.save_book(self, title, author)
        book = Book.objects.get(title=title, author=author)
        self.assertEqual(book.title, title)
        self.assertEqual(book.author, author)
