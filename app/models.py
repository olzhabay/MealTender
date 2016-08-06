from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.IntegerField()
    restaurant = models.OneToOneField('Restaurant', blank=True, null=True)

    def __unicode__(self):
        return self.user.username


class Address(models.Model):
    street = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)

    def __unicode__(self):
        return str(self.lat) + str(self.lng)


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey('Address', blank=True, null=True)
    menu = models.ManyToManyField('Food')

    def __unicode__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=100)
    spiciness = models.IntegerField(default=0)
    is_noodle = models.BooleanField(default=False)
    is_soup = models.BooleanField(default=False)
    is_bibimbab = models.BooleanField(default=False)
    is_pizza = models.BooleanField(default=False)
    is_beef = models.BooleanField(default=False)
    is_pork = models.BooleanField(default=False)
    is_fish = models.BooleanField(default=False)
    is_halal = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    servings = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    ingredients = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey('Profile', blank=True, null=True)
    total_price = models.IntegerField()
    food_list = models.ManyToManyField('Food')
    shipping_address = models.ForeignKey('Address', blank=True, null=True)

    def __unicode__(self):
        return self.customer.user.username
