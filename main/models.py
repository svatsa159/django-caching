from django.db import models
from mongoengine import *
class Variable(models.Model):
    value = models.IntegerField()
    photo = models.TextField(default="")

class DataMongo(Document):
    name = StringField(max_length=200)
    cached = IntField(default=0)