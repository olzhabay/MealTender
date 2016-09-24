from __future__ import unicode_literals

import json
import urllib2

from django.contrib.gis.geos import Point
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from MealTender.settings import GOOGLE_API_KEY, MEDIA_URL


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.IntegerField()
    restaurant = models.OneToOneField('Restaurant', blank=True, null=True)

    def __unicode__(self):
        return self.user.username


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    latlng = models.PointField(null=False, blank=False, srid=4326, verbose_name="Location")
    menu = models.ManyToManyField('Food')
    image = models.ImageField(upload_to=MEDIA_URL, blank=True, null=True)

    def save(self):
        location = "%s %s" % (self.street, self.city)
        location = location.replace(" ", "+")
        if not self.latlng:
            self.geocode(location)
        super(Restaurant, self).save()

    def geocode(self, location):
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (location, GOOGLE_API_KEY)
        response = urllib2.urlopen(url)
        data = json.load(response)
        if data['status'] == 'OK':
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            latlng = Point(latitude, longitude)
            self.latlng = latlng

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
    image = models.ImageField(upload_to=MEDIA_URL, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey('Profile', blank=True, null=True)
    total_price = models.IntegerField()
    food_list = models.ManyToManyField('Food')
    shipping_address = models.CharField(max_length=100)

    def __unicode__(self):
        return self.customer.user.username
