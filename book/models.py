from django.db import models

class Book(models.Model):
    title = models.TextField(max_length=250)
    author = models.TextField(max_length=250)
