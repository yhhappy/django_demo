from django.db import models


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.BooleanField()
