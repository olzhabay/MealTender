from __future__ import print_function
import datetime
import urllib2

import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, render_to_response
from django.template.context import RequestContext
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from MealTender.settings import GOOGLE_API_KEY
from app.forms.user_forms import UserForm, ProfileForm, UserFormEdit
from app.models import Profile, Food, Restaurant
from django.contrib.auth.models import User
from carton.cart import Cart


# general view
def index(request):
    today = datetime.datetime.now().date()
    return render(request, "app/index.html", {"today": today})


def login_user(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Account disabled")
        else:
            print("Invalid login details: {0} {1}".format(username, password))
            return HttpResponse("Invalid login details")
    else:
        return render_to_response('app/login.html', {}, context)


@login_required
def logout_user(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect('/')


@login_required
def profile(request):
    context = RequestContext(request)
    user = User.objects.get(username=request.user)
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = None
    return render_to_response('app/profile.html',
                              {'user': user, 'profile': profile},
                              context)


@login_required
def edit_profile(request):
    context = RequestContext(request)
    edited = False
    user = User.objects.get(username=request.user)
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = None
    user_form = UserFormEdit(instance=user)
    profile_form = ProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = UserFormEdit(data=request.POST, instance=user)
        profile_form = ProfileForm(data=request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = User.objects.get(pk=user.pk)
            profile.save()
            edited = True
    return render_to_response('app/profile_edit.html',
                              {'user_form': user_form, 'profile_form': profile_form, 'edited': edited},
                              context)


def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_from = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_from.is_valid():
            # saving user
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # saving users profile
            profile = profile_from.save(commit=False)
            profile.user = User.objects.get(pk=user.pk)
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_from.errors)
    else:
        user_form = UserForm()
        profile_from = ProfileForm()

    return render_to_response('app/register.html',
                              {'user_form': user_form, 'profile_form': profile_from, 'registered': registered},
                              context)


# restaurant view
def register_restaurant(request):
    return HttpResponse()


def register_food(request):
    return HttpResponse()


def view_orders(request):
    return HttpResponse()


# client view
def search(request):
    context = RequestContext(request)
    if request.method == 'POST':
        address = request.POST['address']
        address = address.replace(" ", "+")
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (address, GOOGLE_API_KEY)
        response = urllib2.urlopen(url)
        data = json.load(response)
        if data['status'] == 'OK':
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            ref_location = Point(latitude, longitude)
            ref_distance = 5000
            restaurants = Restaurant.objects.filter(latlng__distance_lt=(ref_location, Distance(km=ref_distance)))
            if restaurants.count() > 0:
                return render_to_response('app/restaurant_list.html',
                                          {'restaurants': restaurants, 'found': True},
                                          context)
        return render_to_response('app/restaurant_list.html',
                                  {'restaurants': None, 'found': False},
                                  context)


def food_list(request, value=None):
    context = RequestContext(request)
    if value is None:
        foods = Food.objects.all()
    else:
        foods = Food.objects.filter(restaurant=value)
    return render_to_response('app/food_list.html', {'foods': foods}, context)


def make_order(request):
    return HttpResponse()


def show_cart(request):
    return render(request, 'app/show_cart.html')


def add_to_cart(request):
    cart = Cart(request.session)
    food = Food.objects.get(id=request.GET.get('food_id'))
    cart.add(food, price=food.price)
    return HttpResponse("Added")


def remove_from_cart(request):
    cart = Cart(request.session)
    food = Food.objects.get(id=request.GET.get('food_id'))
    cart.remove(food)
    return HttpResponse("Removed")
