from django.shortcuts import render
from django.http import HttpResponse

from . import mozilla, microsoft

# Create your views here.


def homePageView(request):
    microsoft.update()
    mozilla.update()
    return HttpResponse("Hello World!")
