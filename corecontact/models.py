from django.db import models
from .managers import PeopleManager, ContactManager


class People(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    height = models.IntegerField()

    objects = PeopleManager()


class Contacts(models.Model):
    email = models.EmailField()
    number = models.CharField(max_length=20)
    people = models.ForeignKey(People, on_delete=models.CASCADE)

    objects = ContactManager()
