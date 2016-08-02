from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.IntegerField()
    restaurants = models.ForeignKey('Restaurant', blank=True, null=True)
    address = models.ForeignKey('Address', blank=True, null=True)

    def __unicode__(self):
        return self.user.username


class Address(models.Model):
    street = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey('Address')
    menu = models.ManyToManyField('Food')


class Food(models.Model):
    name = models.CharField(max_length=100)
    servings = models.IntegerField()
    price = models.IntegerField()
    ingredients = models.CharField(max_length=250)


class Order(models.Model):
    total_price = models.IntegerField()
    food_list = models.ManyToManyField('Food')
    shipping_address = models.ForeignKey('Address')
