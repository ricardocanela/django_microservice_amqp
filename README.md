# Hello, wellcome to the project:  
# Django as microservice with RabbitMq and Nameko

## What is it about?

> This is a tutorial for usage of [Django framework](https://www.djangoproject.com/) running microservices with [RabbitMq](https://www.rabbitmq.com/) as message broker, using the python framework for building microservices [Nameko](https://github.com/nameko/nameko)

> The goal of this tutorial is to show how you can use Django, it's ORM (Object-Relational Mapper) and all Django features to develop microservices capable of communicate via AMQP (Advanced Message Queuing Protocol) with RabbitMq through RPC (remote procedure call) and Events call (pub-sub) using Nameko framework 

> This project is motivated by the benefits of a microservice communicating using AMQP, you can read more in this [nginx](https://www.nginx.com/blog/building-microservices-inter-process-communication/) article

----
## Tutorial 
For this tutorial you must have installed django, nameko and docker

> $ pip install Django  
> $ pip install nameko  
> $ pip install docker


Create a django project  

> $ django-admin startproject book_microservice

Create a django app

>  $ cd book_microservice  
$ django-admin startapp book

Insert you app on INSTALLED_APPS in book\_microservice/settings.py


> INSTALLED_APPS = [  
    'django.contrib.admin',  
     ...  
    'django.contrib.staticfiles',  
    'book',  
]

In book/models.py

> from django.db import models   

> class Book(models.Model):   
    title = models.TextField(max_length=250)   
    author = models.TextField(max_length=250)

Save your model and run

> $ python manage.py makemigrations  
> $ python manage.py migrate

In book/views.py



> from nameko.rpc import rpc  
from book.models import Book  


>class DjangoService(object):  
    name = "book_service"  

>    @rpc  
    def first_book(self):  
        return Book.objects.first().title  

>    @rpc  
    def last_book(self):  
        return Book.objects.last().title  

>    @rpc  
    def save_book(self, title, author):  
        book = Book()  
        book.title = title  
        book.author = author  
        book.save()  


Now, in the same directory as manage.py, create a file with name run_services.py

> import os  
import django  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_microservice.settings")  
django.setup()  

>from book.views import DjangoService

## Running a RabbitMq instance

The easiest way to run RabbitMq is using docker with this command:

> $ docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management

## Running the microservice

Now you can launch your services using

> $ nameko run run_services --broker amqp://guest:guest@localhost

Your console must look like

> starting services: book_service  
Connected to amqp://guest:**@127.0.0.1:5672//

In another terminal you can run a nameko shell to run the rpc's of your microservices

> $ nameko shell   

>n.rpc.book_service.save_book('title1','author1')  
> book = n.rpc.book_service.first_book()  
> print(book)
>
> out: 'title1'

this nameko shell shows how you can make a rpc call over the amqp, wich can also be done by another python aplication, as an API, using Nameko

## Tests

You can unit test your view in book/test

> from django.test import TestCase  
from .models import Book  
from .views import DjangoService  

>class ServiceTestCase(TestCase):  
    def setUp(self):  
        Book.objects.create(title='title_test', author='author_test')  

>    def test_first_book(self):  
        book = Book.objects.first()  
        self.assertEqual(DjangoService.first_book(self), book.title)  

>    def test_save_book(self):  
        title = 'title_test2'  
        author = 'author_test2'  
        DjangoService.save_book(self, title, author)  
        book = Book.objects.get(title=title, author=author)  
        self.assertEqual(book.title, title)  
        self.assertEqual(book.author, author)  

and run

> python manage.py test

> out:  
Ran 2 tests in 0.006s  
OK


## notes
If you wish to send your data as json, you can use [djangorestframework](http://www.django-rest-framework.org/)'s serializer.

Read more about RPC and Events (pub-sub) in [this](https://docs.nameko.io/en/stable/built_in_extensions.html) nameko documentation 
