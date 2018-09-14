# Hello, wellcome to the project: django as microservice with AMQP (Advanced Message Queuing Protocol )

----
## What is it about?

> This is a template for usage of [Django framework](https://www.djangoproject.com/) running microservices with [RabbitMq](https://www.rabbitmq.com/) as message broker, using the python framework for building microservices [nameko](https://github.com/nameko/nameko)

> This project is motivated on the benefits of a microservice communicating using AMQP, you can read about in this [nginx](https://www.nginx.com/blog/building-microservices-inter-process-communication/) article

----
## Tutorial 
For this tutorial you must have installed django, nameko and docker

Create a django project  

> django-admin startproject book_microservice

Create a django app

>  cd book_microservice  
django-admin startapp book

Insert you app on INSTALLED_APPS in book\_microservice/settings.py


> !# book\_microservice/settings.py  
INSTALLED_APPS = [  
    'django.contrib.admin',  
     ...  
    'django.contrib.staticfiles',  
    'book',  
]

In book/models.py

> from django.db import models   

>class Book(models.Model):   
    title = models.TextField(max_length=250)   
    author = models.TextField(max_length=250)

Save your model and run

> python manage.py makemigrations  
> python manage.py migrate

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

> docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management

## Running the microservice

Now you can launch your services using

> nameko run run_services --broker amqp://guest:guest@localhost

Your console must look like

> starting services: book_service  
Connected to amqp://guest:**@127.0.0.1:5672//

In another terminal you can run a nameko shell to run the rpc's of your microservices

> nameko shell  
> n.rpc.book_service.save_book('title1','author1')  
> book = n.rpc.book_service.first_book()  
> print(book)
>
> out: 'title1'
