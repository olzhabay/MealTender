from __future__ import unicode_literals

import urllib
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


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
        location = "%s, %s, %s, %s" % (self.street, self.city, self.zip_code, self.zip_code)
        if not self.lat or not self.lng:
            result = self.geocode(location)
            result = result.split(',')
            self.lat = result[0]
            self.lng = result[1]
        super(Address, self).save()

    def geocode(self, location):
        output = "csv"
        location = urllib.quote_plus(location)
        request = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % \
                  (location, output, settings.GOOGLE_API_KEY)
        data = request.urlopen(request).read()
        dlist = data.split(',')
        if (dlist[0]) == '200':
            return "%s,%s" % (dlist[2], dlist[3])
        else:
            return ','

    def __unicode__(self):
        return str(self.lat) + str(self.lng)


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
