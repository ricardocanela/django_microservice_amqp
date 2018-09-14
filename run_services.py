import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_microservice.settings")
django.setup()

from book.views import DjangoService
