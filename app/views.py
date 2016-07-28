import datetime

import requests
from django.shortcuts import render, HttpResponse


# general view
def index(request):
    today = datetime.datetime.now().date()
    return render(request, "app/index.html", {"today": today})


def profile(request):
    req = requests.get('https://api.github.com/users/olzhabay')
    content = req.text
    return HttpResponse(content)


def registration(request):
    return HttpResponse()


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