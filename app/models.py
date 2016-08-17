from __future__ import unicode_literals

import json as jsonlib
import urllib2
from django.core.serializers import json
from django.db import models
from django.contrib.auth.models import User
from MealTender.settings import GOOGLE_API_KEY

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
    lat = models.FloatField(editable=False)
    lng = models.FloatField(editable=False)

    def save(self):
        location = '+'.join(filter(None, (self.street, self.city, self.country)))
        location = location.replace(" ", "+")
        if not self.lat or not self.lng:
            self.geocode(location)
        super(Address, self).save()

    def geocode(self, location):
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (location, GOOGLE_API_KEY)
        response = urllib2.urlopen(url)
        data = jsonlib.load(response)
        if data['status'] == 'OK':
            self.lat = data['results'][0]['geometry']['location']['lat']
            self.lng = data['results'][0]['geometry']['location']['lng']


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey('Address', blank=True, null=True)
    menu = models.ManyToManyField('Food')
    image = models.ImageField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=100)
    spiciness = models.IntegerField(default=0)
    is_noodle = models.BooleanField(default=False)
    is_soup = models.BooleanField(default=False)
    is_bibimbab = models.BooleanField(default=False)
    is_pizza = models.BooleanField(default=False)
    is_tteokbokki = models.BooleanField(default=False)
    is_beef = models.BooleanField(default=False)
    is_pork = models.BooleanField(default=False)
    is_fish = models.BooleanField(default=False)
    is_chicken = models.BooleanField(default=False)
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
