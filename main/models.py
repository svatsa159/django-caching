from django.db import models

class Variable(models.Model):
    value = models.IntegerField()
    photo = models.TextField(default="")