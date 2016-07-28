import datetime

import requests
from django.shortcuts import render, HttpResponse


def index(request):
    today = datetime.datetime.now().date()
    return render(request, "app/index.html", {"today": today})


def profile(request):
    req = requests.get('https://api.github.com/users/olzhabay')
    content = req.text
    return HttpResponse(content)
