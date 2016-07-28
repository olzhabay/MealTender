from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.IntegerField('Phone')
    address = models.ForeignKey(Address)
    REQUIRED_FIELDS = ['phone_number', 'address']

    def __unicode__(self):
        return self.email


class Address(models.Model):
    person = models.ForeignKey(User)
    street = models.CharField('Street', max_length=100)
    zip_code = models.CharField('Zip', max_length=10)
    city = models.CharField('City', max_length=20)
    country = models.CharField('Country', max_length=20)


class Restaurant(models.Model):
    name = models.CharField('Restaurant name', max_length=100)
    address = models.ForeignKey(Address)


class Food(models.Model):
    name = models.CharField('Food name', max_length=100)
    servings = models.IntegerField('Servings number')
    price = models.IntegerField('Price')
    ingredients = models.CharField('Ingredients', max_length=250)
