from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class Person(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    address = models.ForeignKey('Address', null=False)
    restaurants = models.ForeignKey('Restaurant', null=False)

    def __unicode__(self):
        return self.email


class Address(models.Model):
    street = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey('Address', null=False)
    menu = models.ManyToManyField('Food')


class Food(models.Model):
    name = models.CharField(max_length=100)
    servings = models.IntegerField()
    price = models.IntegerField()
    ingredients = models.CharField(max_length=250)
