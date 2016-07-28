from __future__ import print_function
import datetime

import requests
from django.shortcuts import render, HttpResponse, RequestContext, render_to_response
from app.forms.user_forms import UserForm, ProfileForm


# general view
def index(request):
    today = datetime.datetime.now().date()
    return render(request, "app/index.html", {"today": today})


def login(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']


def profile(request):
    req = requests.get('https://api.github.com/users/olzhabay')
    content = req.text
    return HttpResponse(content)


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
            profile = profile_from.save()
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_from.errors)
    else:
        user_form = UserForm()
        profile_from = ProfileForm()

    return render_to_response('app/register.html',
                              {'user_form':user_form, 'profile_form':profile_from, 'registered':registered},
                              context)


# restaurant view
def register_restaurant(request):
    return HttpResponse()


def register_food(request):
    return HttpResponse()


def view_orders(request):
    return HttpResponse()


# client view
def view_restaurants(request):
    return HttpResponse()


def view_menu(request):
    return HttpResponse()


def view_food(request):
    return HttpResponse()


def make_order(request):
    return HttpResponse()


def view_cart(request):
    return HttpResponse()
